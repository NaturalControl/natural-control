# The action gate wraps every tool call

The AI agent (Hermes) never calls tools, Composio, or Google directly. Every tool call goes through our action gate, which lets read-only calls through and holds consequential ones until the user approves the exact action, read back from the call itself rather than from the agent's description. We chose this over relying on the agent's own approval requests because a check outside the model is the only way "approval before every consequential action" is a guarantee rather than a hope; Anthropic's Claude Code auto mode puts its permission check in the harness for the same reason.

## Consequences

- Gmail and Calendar tools run through the Composio SDK with the gate in its before-execute hook and verification in its after-execute hook. Connecting Hermes straight to Composio's MCP server would skip those hooks, so that is not allowed.
- Browser Use clicks happen inside its own loop, so the POC must show the gate can intercept consequential browser actions. If it can't, the browser becomes read-only for the initial release.
