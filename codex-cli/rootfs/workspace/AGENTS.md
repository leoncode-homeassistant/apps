# Home Assistant workspace rules

- Use `/homeassistant` as the canonical Home Assistant configuration path.
  `/config` is only a compatibility symlink.
- Read the existing configuration before editing it and preserve its include
  structure, naming conventions, and formatting choices.
- Prefer the `home_assistant` MCP tools for states, devices, entities,
  services, automations, and integrations.
- Require explicit confirmation before deletions, restores, restarts, or other
  destructive and disruptive actions.
- Create a current backup before broad configuration changes.
- Validate configuration changes before restarting Home Assistant.
- Never store credentials, private MCP paths, or tokens in Git or visible logs.
