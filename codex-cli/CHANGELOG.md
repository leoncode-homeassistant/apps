# Changelog

## 0.1.0

- Initial release in the LeonCode Home Assistant Apps repository.
- Includes Codex CLI 0.146.1 with persistent authentication and configuration.
- Provides SSH access using public keys only.
- Mounts the Home Assistant configuration read-write at `/homeassistant`.
- Provides `/config` as a compatibility symlink to `/homeassistant`.
- Supports an optional HA-MCP Streamable HTTP endpoint.
- Includes the corrected native `bashio` validation for `authorized_keys`.
- Publishes multi-architecture images for `amd64` and `aarch64`.
