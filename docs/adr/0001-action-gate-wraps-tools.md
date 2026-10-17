# The action gate wraps every tool call

The proposed Hermes integration sends every tool call through our action gate. Navigation and temporary preparation may proceed when they have no consequential effect. Writes and consequential commitments require approval of exact details from the proposed call. FR24 defines the narrow exception for rejecting non-essential cookies. The gate blocks new task actions while work is paused.

This check belongs outside the planning model. The POC must verify that the integration enforces it on every action path.

## Consequences

- Gmail and Calendar tools run through the Composio SDK with the gate in its before-execute hook and verification in its after-execute hook. Connecting Hermes straight to Composio's MCP server would skip those hooks, so that is not allowed.
- Browser Use clicks happen inside its own loop, so the POC must show the gate can intercept consequential browser actions. If it can't, the browser becomes read-only for the initial release.
