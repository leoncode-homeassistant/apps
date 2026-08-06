# Home Assistant workspace

You are running inside the Codex CLI app container on Home Assistant OS. The
project selected by the user is `/workspace`; it is an orientation directory
that exposes the Home Assistant data mounted into this container.

## Workspace layout

- `/workspace/homeassistant` -> `/homeassistant`: canonical Home Assistant
  configuration directory. `/config` is a compatibility symlink to the same
  location.
- `/workspace/backup` -> `/backup`: Home Assistant backups available to this
  app.
- `/workspace/share` -> `/share`: Home Assistant shared data.
- `/data/codex`: persistent Codex configuration, authentication, plugins, and
  other Codex state. Do not expose credentials from this directory.

This container does not have unrestricted access to the Home Assistant host,
Supervisor internals, other app containers, or the Docker socket. Do not assume
that a command executed here runs on the Home Assistant host.

## How to work here

- Treat requests in this project as Home Assistant tasks unless the user says
  otherwise.
- Inspect the existing configuration before editing it. Preserve its include
  structure, naming conventions, comments, secrets usage, and formatting.
- Use the configured `home_assistant` MCP server for live states, devices,
  entities, services, automations, and integrations when its tools are
  available. If it is unavailable or lacks a required operation, explain the
  limitation instead of pretending to have changed live Home Assistant state.
- Use `/homeassistant` for file changes. Avoid editing `.storage` directly
  unless the user explicitly requests it and the consequences are understood.
- Keep credentials, tokens, private MCP URLs, and secret values out of replies,
  logs, Git, and newly created files. Preserve `!secret` references.
- Review diffs and validate Home Assistant configuration changes before any
  restart or reload. State clearly when validation cannot be performed from
  this container.
- Obtain explicit confirmation before deleting devices or entities, restoring
  backups, restarting Home Assistant, or performing another destructive or
  disruptive action.
- Create or recommend a current backup before broad or risky configuration
  changes.

When the user asks where files are located, answer with the canonical paths
above. You do not need the user to explain this container layout again.
