import { describe, expect, it } from "vitest";

import { encodeCommand, isStopShortcut } from "./controls";

const key = (k: string, mods: Partial<Record<"altKey" | "ctrlKey" | "metaKey", boolean>> = {}) => ({
  key: k,
  altKey: false,
  ctrlKey: false,
  metaKey: false,
  ...mods,
});

describe("isStopShortcut", () => {
  it("accepts a bare Escape", () => {
    expect(isStopShortcut(key("Escape"))).toBe(true);
  });

  it("ignores Escape combined with VoiceOver-style modifiers", () => {
    expect(isStopShortcut(key("Escape", { ctrlKey: true, altKey: true }))).toBe(false);
  });

  it("ignores other keys", () => {
    expect(isStopShortcut(key("s"))).toBe(false);
  });
});

describe("encodeCommand", () => {
  it("encodes the plain command word the worker expects", () => {
    expect(new TextDecoder().decode(encodeCommand("stop"))).toBe("stop");
  });
});
