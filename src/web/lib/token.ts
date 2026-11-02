import { AccessToken } from "livekit-server-sdk";

export interface SessionToken {
  serverUrl: string;
  roomName: string;
  participantToken: string;
}

export class MissingConfigError extends Error {}

type Env = Record<string, string | undefined>;

/**
 * Mint a short-lived token for one voice session in a fresh room.
 * The agent worker joins the same room through LiveKit's automatic dispatch.
 */
export async function createSessionToken(env: Env = process.env): Promise<SessionToken> {
  const serverUrl = env.LIVEKIT_URL;
  const apiKey = env.LIVEKIT_API_KEY;
  const apiSecret = env.LIVEKIT_API_SECRET;
  if (!serverUrl || !apiKey || !apiSecret) {
    throw new MissingConfigError("LiveKit is not configured on the server");
  }

  const suffix = crypto.randomUUID().slice(0, 8);
  const roomName = `nc-${suffix}`;
  const token = new AccessToken(apiKey, apiSecret, {
    identity: `user-${suffix}`,
    ttl: "15m",
  });
  token.addGrant({
    room: roomName,
    roomJoin: true,
    canPublish: true,
    canSubscribe: true,
    canPublishData: true,
  });
  return { serverUrl, roomName, participantToken: await token.toJwt() };
}
