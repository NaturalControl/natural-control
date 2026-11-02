"use client";

import { Room, RoomEvent, Track } from "livekit-client";
import { useCallback, useEffect, useRef, useState } from "react";

import { CONTROL_TOPIC, type ControlCommand, encodeCommand, isStopShortcut } from "@/lib/controls";
import type { SessionToken } from "@/lib/token";

type Status = "idle" | "connecting" | "connected" | "error";

const STATUS_TEXT: Record<Status, string> = {
  idle: "Not connected.",
  connecting: "Connecting.",
  connected: "Connected. Speak to start a task.",
  error: "Could not connect. Try again.",
};

/**
 * Session controls: start/end the voice session and send work-stop commands.
 * Status changes are announced politely; stop confirmations assertively, because the
 * user needs to know at once that the stop was sent (FR.Sa.5).
 */
export function SessionControls() {
  const roomRef = useRef<Room | null>(null);
  const [status, setStatus] = useState<Status>("idle");
  const [urgent, setUrgent] = useState("");

  const send = useCallback(async (command: ControlCommand) => {
    const room = roomRef.current;
    if (!room) return;
    await room.localParticipant.publishData(encodeCommand(command), {
      reliable: true,
      topic: CONTROL_TOPIC,
    });
    setUrgent(`${command[0].toUpperCase()}${command.slice(1)} sent.`);
  }, []);

  const start = useCallback(async () => {
    setStatus("connecting");
    try {
      const response = await fetch("/api/token", { method: "POST" });
      if (!response.ok) throw new Error(`token request failed: ${response.status}`);
      const { serverUrl, participantToken } = (await response.json()) as SessionToken;

      const room = new Room();
      room.on(RoomEvent.TrackSubscribed, (track) => {
        if (track.kind === Track.Kind.Audio) document.body.appendChild(track.attach());
      });
      room.on(RoomEvent.Disconnected, () => {
        roomRef.current = null;
        setStatus("idle");
      });
      await room.connect(serverUrl, participantToken);
      await room.localParticipant.setMicrophoneEnabled(true);
      roomRef.current = room;
      setStatus("connected");
    } catch {
      setStatus("error");
    }
  }, []);

  const end = useCallback(async () => {
    await roomRef.current?.disconnect();
  }, []);

  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (isStopShortcut(event)) {
        event.preventDefault();
        void send("stop");
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [send]);

  useEffect(() => () => void roomRef.current?.disconnect(), []);

  const connected = status === "connected";
  return (
    <section aria-labelledby="session-heading">
      <h2 id="session-heading">Session</h2>
      <p role="status">{STATUS_TEXT[status]}</p>
      <p role="alert">{urgent}</p>

      {connected ? (
        <button type="button" onClick={end}>
          End session
        </button>
      ) : (
        <button type="button" onClick={start} disabled={status === "connecting"}>
          Start session
        </button>
      )}

      <h2>Task controls</h2>
      <p>Press Escape at any time to stop work. The task pauses and keeps its progress.</p>
      <button type="button" onClick={() => send("stop")} disabled={!connected}>
        Stop working
      </button>
      <button type="button" onClick={() => send("resume")} disabled={!connected}>
        Resume
      </button>
      <button type="button" onClick={() => send("cancel")} disabled={!connected}>
        Cancel task
      </button>
    </section>
  );
}
