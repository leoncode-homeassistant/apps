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
codex_provider: custom
codex_provider_name: OmniRoute
codex_base_url: "https://omniroute.leonapi.de/v1"
codex_model: gpt-5.6-sol
codex_api_key: null
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

### `codex_provider`

Select `custom` to use an OpenAI-compatible Responses API such as OmniRoute.
Select `openai` to use Codex's built-in OpenAI provider directly.

With `openai`, the custom provider name and base URL are ignored. You can sign
in with ChatGPT or enter an OpenAI Platform API key. No proxy is involved.

### `codex_provider_name`

The display name of the custom provider. The default is `OmniRoute`. This
setting is ignored when `codex_provider` is set to `openai`.

### `codex_base_url`

The custom provider's Responses API base URL. The default is
`https://omniroute.leonapi.de/v1`. This setting is ignored when
`codex_provider` is set to `openai`.

### `codex_model`

This optional model identifier is sent to the selected provider. The default
is `gpt-5.6-sol`, matching the repository maintainer's OmniRoute configuration.
Leave it empty to let Codex select its own default. When set, the selected
provider must support the configured model identifier.

### `codex_api_key`

This optional password field provides a convenient way to authenticate during
app startup. Enter the API key for the selected provider. With `custom`, this
is the custom provider's key; with `openai`, it is an OpenAI Platform API key.

When the field is set, the app passes the key to the official
`codex login --with-api-key` command through standard input. Codex stores the
resulting authentication persistently under `/data/codex`. The key is never
written to the generated `config.toml`, container image, repository, or logs.

The password field masks the value in the Home Assistant interface, but the
value remains part of the app configuration and may be included in Home
Assistant backups. Leave it empty if you prefer to authenticate through the
Codex desktop dialog or interactively inside the SSH session.

When this field is empty and Codex desktop asks you to authenticate the remote
CLI, choose **Enter API key** and enter the key belonging to the selected
provider. For OmniRoute, enter your OmniRoute key, not an OpenAI Platform key.
Do not choose **Continue with ChatGPT** when `custom` is selected. ChatGPT
subscription authentication is intended for the direct OpenAI provider.

### `allow_tcp_forwarding`

Keep this disabled unless SSH port forwarding is explicitly required. Enabling
it expands what an authenticated SSH client can reach through the app.

## Start and connect

The default host port is `2222`. The app provides the `root` SSH account only;
your computer's local username will not exist inside the container. After
starting the app, connect with:

```bash
ssh -p 2222 -i ~/.ssh/id_ed25519_homeassistant root@homeassistant.local
```

If the log reports `Invalid user`, explicitly set the SSH user to `root` in
your command or SSH host configuration.

Authenticate Codex once inside the app:

```bash
codex login --with-api-key
```

When connecting through Codex desktop, its authentication dialog performs the
same persistent remote login. You normally do not need to run the command
manually.

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
