"""Resolve the reddit skill root (directory that contains SKILL.md).

Credentials live in ``.env`` next to SKILL.md — same place the skill is
registered (Cursor ``~/.cursor/skills/reddit``, Hermes, etc.).
"""

from __future__ import annotations

from pathlib import Path


def get_skill_home() -> Path:
    """Return the skill directory that contains ``SKILL.md``."""
    here = Path(__file__).resolve().parent
    for candidate in (here, *here.parents):
        if (candidate / "SKILL.md").is_file():
            return candidate
    return here


def display_skill_home() -> str:
    """Return a user-friendly ``~/``-shortened path to the skill root."""
    home = get_skill_home()
    try:
        return "~/" + str(home.relative_to(Path.home()))
    except ValueError:
        return str(home)


def env_path() -> Path:
    """Path to the skill-local ``.env`` file."""
    return get_skill_home() / ".env"
