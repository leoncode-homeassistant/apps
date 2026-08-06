# Codex CLI for Home Assistant OS

Codex CLI turns your Home Assistant OS installation into a persistent remote
Codex workspace. Connect from a terminal or from Codex desktop over SSH, work
directly with the Home Assistant configuration, and optionally expose Home
Assistant operations to Codex through HA-MCP.

## Before you install

You need:

- Home Assistant OS or Home Assistant Supervised;
- an SSH key pair on the computer running Codex desktop;
- optionally, the [HA-MCP](https://github.com/homeassistant-ai/ha-mcp) app or
  custom component.

The app intentionally does not receive the Docker socket or unrestricted host
access. It does receive read-write access to the Home Assistant configuration,
backups, and shared data.

## Configuration

```yaml
authorized_keys:
  - ssh-ed25519 AAAA... your-name
ha_mcp_url: "http://192.168.1.20:9583/private_YOUR_SECRET_PATH"
allow_tcp_forwarding: false
```

### `authorized_keys`

Add at least one complete public SSH key. Password authentication is disabled
and cannot be enabled through the app configuration.

Generate a dedicated key if needed:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_homeassistant
cat ~/.ssh/id_ed25519_homeassistant.pub
```

### `ha_mcp_url`

This option is optional. Paste the local connection URL shown by HA-MCP. The
private path is a credential: keep it in the Home Assistant app configuration,
never commit it to Git, and rotate it if it is exposed.

When configured, the app maintains a `home_assistant` MCP server entry in
`/data/codex/config.toml`.

### `allow_tcp_forwarding`

Keep this disabled unless SSH port forwarding is explicitly required. Enabling
it expands what an authenticated SSH client can reach through the app.

## Start and connect

The default host port is `2222`. After starting the app, connect with:

```bash
ssh -p 2222 -i ~/.ssh/id_ed25519_homeassistant root@homeassistant.local
```

Authenticate Codex once inside the app:

```bash
codex login --device-auth
```

Codex authentication and configuration are stored under `/data/codex` and
survive app updates.

## Connect from Codex desktop

Add a host to `~/.ssh/config` on the computer running Codex desktop:

```sshconfig
Host homeassistant-codex
  HostName homeassistant.local
  Port 2222
  User root
  IdentityFile ~/.ssh/id_ed25519_homeassistant
  IdentitiesOnly yes
```

Verify the connection first:

```bash
ssh homeassistant-codex
```

Then add `homeassistant-codex` under **Settings → Connections** in Codex
desktop and open `/workspace` as the remote project.

## Workspace layout

| Path | Purpose |
| --- | --- |
| `/workspace` | Default Codex project directory |
| `/workspace/homeassistant` | Link to the Home Assistant configuration |
| `/homeassistant` | Canonical Home Assistant configuration path |
| `/config` | Compatibility link to `/homeassistant` |
| `/workspace/backup` | Home Assistant backups |
| `/workspace/share` | Home Assistant shared directory |
| `/data/codex` | Persistent Codex authentication and configuration |

## Verify HA-MCP

After changing `ha_mcp_url`, restart the app and run:

```bash
codex mcp list
```

The `home_assistant` server should appear. If HA-MCP rotates its private path,
update the app option and restart the app again.

## Security recommendations

- Never expose port `2222` directly to the public internet.
- Use a trusted LAN, WireGuard, Tailscale, or another VPN for remote access.
- Use a dedicated SSH key for this app.
- Create a current backup before broad configuration changes.
- Review diffs and validate the Home Assistant configuration before restarting.
- Require explicit confirmation for deletion, restoration, restart, and other
  disruptive operations.
- Rotate the HA-MCP private path if it appears in a screenshot or log.

## Updates

Home Assistant detects updates through the version in `config.yaml`. The
repository publishes a matching multi-architecture image for each release.
Codex state under `/data` is retained during normal updates.
