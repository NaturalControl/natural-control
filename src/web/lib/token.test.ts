import { describe, expect, it } from "vitest";

import { createSessionToken, MissingConfigError } from "./token";

const env = {
  LIVEKIT_URL: "wss://example.livekit.cloud",
  LIVEKIT_API_KEY: "APItest",
  LIVEKIT_API_SECRET: "synthetic-secret-at-least-32-characters-long",
};

function claims(jwt: string) {
  return JSON.parse(Buffer.from(jwt.split(".")[1], "base64url").toString());
}

describe("createSessionToken", () => {
  it("grants publish, subscribe and data in a fresh room only", async () => {
    const token = await createSessionToken(env);
    const video = claims(token.participantToken).video;

    expect(token.roomName).toMatch(/^nc-/);
    expect(video).toMatchObject({
      room: token.roomName,
      roomJoin: true,
      canPublish: true,
      canSubscribe: true,
      canPublishData: true,
    });
    expect(video.roomAdmin).toBeUndefined();
  });

  it("uses a different room each time", async () => {
    const [a, b] = await Promise.all([createSessionToken(env), createSessionToken(env)]);
    expect(a.roomName).not.toBe(b.roomName);
  });

  it("does not put the API secret in the response", async () => {
    const token = await createSessionToken(env);
    expect(JSON.stringify(token)).not.toContain(env.LIVEKIT_API_SECRET);
  });

  it("refuses to mint without configuration", async () => {
    await expect(createSessionToken({})).rejects.toBeInstanceOf(MissingConfigError);
  });
});
