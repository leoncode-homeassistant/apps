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
provider = sys.argv[2].strip() if len(sys.argv) > 2 else "custom"
provider_name = sys.argv[3].strip() if len(sys.argv) > 3 else "OmniRoute"
base_url = sys.argv[4].strip() if len(sys.argv) > 4 else "https://omniroute.leonapi.de/v1"
model = sys.argv[5].strip() if len(sys.argv) > 5 else "gpt-5.6-sol"

if provider not in {"custom", "openai"}:
    raise SystemExit(f"Unsupported Codex provider: {provider}")
if provider == "custom" and not provider_name:
    raise SystemExit("A custom provider name is required")
if provider == "custom" and not base_url:
    raise SystemExit("A custom provider base URL is required")

managed_lines = [
    BEGIN,
    'cli_auth_credentials_store = "file"',
]

if model:
    managed_lines.append(f"model = {toml_string(model)}")

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
