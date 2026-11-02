import { createSessionToken, MissingConfigError } from "@/lib/token";

export async function POST() {
  try {
    return Response.json(await createSessionToken(), {
      headers: { "Cache-Control": "no-store" },
    });
  } catch (error) {
    if (error instanceof MissingConfigError) {
      return Response.json({ error: error.message }, { status: 503 });
    }
    throw error;
  }
}
