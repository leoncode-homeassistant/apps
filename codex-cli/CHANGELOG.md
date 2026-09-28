# Changelog

## 0.3.3

- Updates OpenAI Codex CLI from `0.153.4` to `0.158.0`.
## 0.3.2

- Updates OpenAI Codex CLI from `0.146.1` to `0.153.4`.
## 0.3.1

- Expands `/workspace/AGENTS.md` with automatic English orientation for Codex,
  including the container boundary, mounted paths, HA-MCP usage, validation,
  secrets handling, and confirmation requirements.
- Shows the workspace instruction file in the SSH login message.

## 0.3.0

- Adds Home Assistant options for Codex approval policy, sandbox mode, web
  search, response verbosity, reasoning summaries, and reasoning effort.
- Adds a Home Assistant option that allows or disables installed Codex plugins.
- Keeps model-specific and Codex defaults available without forcing overrides.

## 0.2.2

- Installs the Alpine `bubblewrap` package for Codex's Linux sandbox.
- Verifies `bwrap` during the container build so missing sandbox prerequisites fail early.

## 0.2.1

- Uses direct OpenAI with no explicit model as the neutral default.
- Removes all prefilled OmniRoute provider values.
- Uses an empty masked API-key value instead of `null`, allowing Home Assistant to save the configuration without a key.

## 0.2.0

- Adds a selectable Codex model provider.
- Makes the custom provider name, Responses API base URL, and model configurable in Home Assistant.
- Keeps direct OpenAI usage available without requiring any custom provider settings.
- Adds an optional masked API-key field while retaining interactive remote authentication.
- Persists remote Codex authentication under `/data/codex` across app updates.
- Adds a configurable model identifier, defaulting to `gpt-5.6-sol`.
- Keeps provider credentials out of the generated Codex configuration, container image, repository, and logs.

## 0.1.1

- Removes the unsupported `UsePAM` SSH option from the Alpine-based image.
- Clarifies that SSH connections must use the `root` account.

## 0.1.0

- Initial release in the LeonCode Home Assistant Apps repository.
- Includes Codex CLI 0.146.1 with persistent authentication and configuration.
- Provides SSH access using public keys only.
- Mounts the Home Assistant configuration read-write at `/homeassistant`.
- Provides `/config` as a compatibility symlink to `/homeassistant`.
- Supports an optional HA-MCP Streamable HTTP endpoint.
- Includes the corrected native `bashio` validation for `authorized_keys`.
- Publishes multi-architecture images for `amd64` and `aarch64`.
