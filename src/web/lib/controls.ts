/**
 * Keyboard control for stopping work (FR.Sa.1).
 *
 * Provisional: Escape on its own. VoiceOver commands use Control+Option, so a bare
 * Escape does not collide with them. What the stop key does when another app has focus
 * is an open team decision.
 */
export const STOP_KEY = "Escape";

export type ControlCommand = "stop" | "resume" | "cancel";

/** The LiveKit data topic the agent worker listens on for control commands. */
export const CONTROL_TOPIC = "control";

export function isStopShortcut(event: Pick<KeyboardEvent, "key" | "altKey" | "ctrlKey" | "metaKey">) {
  return event.key === STOP_KEY && !event.altKey && !event.ctrlKey && !event.metaKey;
}

export function encodeCommand(command: ControlCommand) {
  return new TextEncoder().encode(command);
}
