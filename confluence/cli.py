#!/usr/bin/env python3
"""Confluence skill helpers — env only.

Use this script to resolve / validate the per-workspace ``.env``.
Run Confluence operations with the real CLI afterward::

    python cli.py env-check
    set -a && source "$(python cli.py env-path)" && set +a
    confluence read 123456789 --format markdown

Install once: ``npm install -g confluence-cli``
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from _skill_home import (  # noqa: E402
    display_env_path,
    display_skill_home,
    env_path,
    preferred_env_path,
)

REQUIRED_HINT = (
    "CONFLUENCE_DOMAIN",
    "CONFLUENCE_API_TOKEN",
)


def _parse_env_file(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        if key.startswith("export "):
            key = key[len("export ") :].strip()
        val = val.strip().strip("'").strip('"')
        if key:
            out[key] = val
    return out


def _print_json(data: Any) -> None:
    print(json.dumps(data, indent=2, default=str))


def cmd_env_path(_: argparse.Namespace) -> int:
    """Print the resolved ``.env`` path (for ``source``)."""
    print(env_path())
    return 0


def cmd_env_check(_: argparse.Namespace) -> int:
    """Show resolved .env + whether confluence-cli is on PATH."""
    resolved = env_path()
    parsed: dict[str, str] = {}
    if resolved.is_file():
        parsed = _parse_env_file(resolved)

    # Merge: process env wins over file for the "effective" check
    effective = {**parsed}
    for key in list(REQUIRED_HINT) + [
        "CONFLUENCE_EMAIL",
        "CONFLUENCE_AUTH_TYPE",
        "CONFLUENCE_API_PATH",
        "CONFLUENCE_READ_ONLY",
    ]:
        if os.environ.get(key, "").strip():
            effective[key] = os.environ[key].strip()

    which = shutil.which("confluence")
    missing = [k for k in REQUIRED_HINT if not effective.get(k, "").strip()]
    _print_json(
        {
            "ok": which is not None and not missing,
            "library": display_skill_home(),
            "env": str(resolved),
            "env_display": display_env_path(),
            "env_exists": resolved.is_file(),
            "preferred_create": str(preferred_env_path()),
            "confluence_cli": which,
            "missing_env": missing,
            "hint_install": None if which else "npm install -g confluence-cli",
            "hint_source": (
                f'set -a && source "{resolved}" && set +a'
                if resolved.is_file()
                else f"Create {preferred_env_path()} from .env.example"
            ),
            "hint_run": "confluence <command> …  # after sourcing .env",
        }
    )
    return 0 if which and not missing else 1


def cmd_print_exports(_: argparse.Namespace) -> int:
    """Print ``export KEY=value`` lines from the resolved ``.env`` (for eval)."""
    resolved = env_path()
    if not resolved.is_file():
        print(f"# missing: {resolved}", file=sys.stderr)
        return 1
    for key, val in _parse_env_file(resolved).items():
        # shell-safe single quotes
        safe = val.replace("'", "'\"'\"'")
        print(f"export {key}='{safe}'")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="confluence-skill",
        description=(
            "Env helpers only. Run Confluence with `confluence …` after sourcing .env."
        ),
    )
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("env-check", aliases=["test"], help="Validate .env + CLI")
    s.set_defaults(func=cmd_env_check)

    s = sub.add_parser("env-path", help="Print resolved .env path")
    s.set_defaults(func=cmd_env_path)

    s = sub.add_parser(
        "print-exports",
        help="Print export lines from .env (eval into the shell)",
    )
    s.set_defaults(func=cmd_print_exports)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
