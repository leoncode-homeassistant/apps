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
managed = ""
if mcp_url:
    managed = "\n".join(
        [
            BEGIN,
            "[mcp_servers.home_assistant]",
            f"url = {toml_string(mcp_url)}",
            END,
        ]
    )

parts = [part for part in (existing, managed) if part]
config_path.write_text("\n\n".join(parts) + ("\n" if parts else ""), encoding="utf-8")
config_path.chmod(0o600)
