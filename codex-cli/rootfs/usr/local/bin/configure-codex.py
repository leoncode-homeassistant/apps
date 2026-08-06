#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys


BEGIN = "# BEGIN HOME ASSISTANT CODEX APP"
END = "# END HOME ASSISTANT CODEX APP"


def toml_string(value: str) -> str:
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'


config_path = pathlib.Path("/data/codex/config.toml")
config_path.parent.mkdir(parents=True, exist_ok=True)
existing = config_path.read_text(encoding="utf-8") if config_path.exists() else ""

start = existing.find(BEGIN)
end = existing.find(END)
if start != -1 and end != -1 and end >= start:
    end += len(END)
    existing = (existing[:start] + existing[end:]).strip()

mcp_url = sys.argv[1].strip() if len(sys.argv) > 1 else ""
provider = sys.argv[2].strip() if len(sys.argv) > 2 else "openai"
provider_name = sys.argv[3].strip() if len(sys.argv) > 3 else ""
base_url = sys.argv[4].strip() if len(sys.argv) > 4 else ""
model = sys.argv[5].strip() if len(sys.argv) > 5 else ""
approval_policy = sys.argv[6].strip() if len(sys.argv) > 6 else "default"
sandbox_mode = sys.argv[7].strip() if len(sys.argv) > 7 else "default"
web_search = sys.argv[8].strip() if len(sys.argv) > 8 else "default"
model_verbosity = sys.argv[9].strip() if len(sys.argv) > 9 else "default"
reasoning_summary = sys.argv[10].strip() if len(sys.argv) > 10 else "default"
reasoning_effort = sys.argv[11].strip() if len(sys.argv) > 11 else "default"
plugins_enabled = sys.argv[12].strip().lower() if len(sys.argv) > 12 else "true"

if provider not in {"custom", "openai"}:
    raise SystemExit(f"Unsupported Codex provider: {provider}")
if provider == "custom" and not provider_name:
    raise SystemExit("A custom provider name is required")
if provider == "custom" and not base_url:
    raise SystemExit("A custom provider base URL is required")

choices = {
    "approval policy": (approval_policy, {"default", "untrusted", "on-request", "never"}),
    "sandbox mode": (sandbox_mode, {"default", "read-only", "workspace-write", "danger-full-access"}),
    "web search mode": (web_search, {"default", "disabled", "cached", "indexed", "live"}),
    "model verbosity": (model_verbosity, {"default", "low", "medium", "high"}),
    "reasoning summary": (reasoning_summary, {"default", "auto", "concise", "detailed", "none"}),
    "reasoning effort": (reasoning_effort, {"default", "minimal", "low", "medium", "high", "xhigh", "ultra"}),
    "plugins enabled": (plugins_enabled, {"true", "false"}),
}
for label, (value, allowed) in choices.items():
    if value not in allowed:
        raise SystemExit(f"Unsupported {label}: {value}")

managed_lines = [
    BEGIN,
    'cli_auth_credentials_store = "file"',
]

if model:
    managed_lines.append(f"model = {toml_string(model)}")

optional_settings = (
    ("approval_policy", approval_policy),
    ("sandbox_mode", sandbox_mode),
    ("web_search", web_search),
    ("model_verbosity", model_verbosity),
    ("model_reasoning_summary", reasoning_summary),
    ("model_reasoning_effort", reasoning_effort),
)
for key, value in optional_settings:
    if value != "default":
        managed_lines.append(f"{key} = {toml_string(value)}")

if provider == "custom":
    managed_lines.extend(
        [
            'model_provider = "custom"',
            "",
            "[model_providers.custom]",
            f"name = {toml_string(provider_name)}",
            f"base_url = {toml_string(base_url)}",
            'wire_api = "responses"',
            "requires_openai_auth = true",
        ]
    )

if mcp_url:
    managed_lines.extend(
        [
            "",
            "[mcp_servers.home_assistant]",
            f"url = {toml_string(mcp_url)}",
        ]
    )

managed_lines.append(END)
managed = "\n".join(managed_lines)

parts = [part for part in (existing, managed) if part]
config_path.write_text("\n\n".join(parts) + ("\n" if parts else ""), encoding="utf-8")
config_path.chmod(0o600)

requirements_path = pathlib.Path("/etc/codex/requirements.toml")
if plugins_enabled == "false":
    requirements_path.parent.mkdir(parents=True, exist_ok=True)
    requirements_path.write_text("[features]\nplugins = false\n", encoding="utf-8")
    requirements_path.chmod(0o644)
else:
    requirements_path.unlink(missing_ok=True)
