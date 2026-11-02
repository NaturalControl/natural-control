"""LiveKit Agents worker: the voice interface (SRS S.1).

Run locally with `uv run --extra voice natural-control-worker dev`.

Speech goes through LiveKit Inference (STT, voice LLM, TTS). The voice LLM only turns
speech into supervision commands (the function tools below); task planning is Hermes.
The client's keyboard stop arrives as a data packet on the "control" topic and is
handled without the LLM, so it does not wait on speech recognition (FR.Sa.1, NFR3).
Ordinary barge-in only interrupts speech; it never stops work.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Coroutine
from typing import Any

from livekit import rtc
from livekit.agents import Agent, AgentServer, AgentSession, JobContext, cli, function_tool

from natural_control.adapters.hermes import HermesGatewayRuntime
from natural_control.config import Settings
from natural_control.session import SupervisionSession

logger = logging.getLogger("natural_control.voice")

INSTRUCTIONS = """\
You are the voice of Natural Control, an assistant for blind and visually impaired users.
You do not do tasks yourself. You pass requests to the task agent with your tools and
report what it says. Keep replies short. Never claim something is done unless a tool
result says it was verified. If the user says "stop" or "stop working", call stop_work.
Only call approve_pending after the user clearly approves the exact details you read back.
"""

server = AgentServer()


class SupervisorAgent(Agent):
    def __init__(self, core: SupervisionSession) -> None:
        super().__init__(instructions=INSTRUCTIONS)
        self._core = core

    @function_tool
    async def start_task(self, request: str) -> str:
        """Start a new task from the user's request."""
        task = await self._core.start_task(request)
        return f"Started task {task.task_id[:6]}."

    @function_tool
    async def stop_work(self) -> str:
        """Pause the running task. Use for "stop", "stop working", "hold on, stop that"."""
        await self._core.stop_work()
        return "Stop handled."

    @function_tool
    async def resume_task(self) -> str:
        """Resume a paused task, only when the user clearly asks to continue."""
        await self._core.resume()
        return "Resume handled."

    @function_tool
    async def cancel_task(self) -> str:
        """End the current task. Earlier actions are not undone."""
        await self._core.cancel()
        return "Cancel handled."

    @function_tool
    async def approve_pending(self) -> str:
        """Approve the action that was just read back, after the user clearly says yes."""
        return "Approved." if self._core.approve_pending() else "Nothing to approve."

    @function_tool
    async def decline_pending(self) -> str:
        """Decline the action that was read back, or the user changed its details."""
        return "Declined." if self._core.decline_pending() else "Nothing to decline."


@server.rtc_session()
async def entrypoint(ctx: JobContext) -> None:
    settings = Settings.from_env()
    session: AgentSession[None] = AgentSession(
        stt=settings.voice_stt, llm=settings.voice_llm, tts=settings.voice_tts
    )
    runtime = HermesGatewayRuntime(settings.agent_model, settings.openrouter_api_key.reveal())

    def say(text: str) -> None:
        session.say(text)

    core = SupervisionSession(runtime, say=say)
    background: set[asyncio.Task[None]] = set()

    def spawn(coro: Coroutine[Any, Any, None]) -> None:
        task = asyncio.create_task(coro)
        background.add(task)
        task.add_done_callback(background.discard)

    @ctx.room.on("data_received")
    def on_control(packet: rtc.DataPacket) -> None:
        if packet.topic != "control":
            return
        command = packet.data.decode(errors="ignore").strip()
        handlers = {"stop": core.stop_work, "resume": core.resume, "cancel": core.cancel}
        handler = handlers.get(command)
        if handler is None:
            logger.warning("unknown control command")
            return
        spawn(handler())

    @ctx.room.on("participant_disconnected")
    def on_left(_participant: rtc.RemoteParticipant) -> None:
        spawn(core.connection_lost())

    await session.start(agent=SupervisorAgent(core), room=ctx.room)
    await ctx.connect()


def main() -> None:
    cli.run_app(server)


if __name__ == "__main__":
    main()
