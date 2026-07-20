"""Resolve the google-workspace skill root (directory that contains SKILL.md).

OAuth credentials live next to SKILL.md — same place the skill is registered
(Cursor ``~/.cursor/skills/google-workspace``, Hermes
``…/skills/productivity/google-workspace``, etc.).
"""

from __future__ import annotations

from pathlib import Path


def get_skill_home() -> Path:
    """Return the skill directory that contains ``SKILL.md``.

    Scripts live in ``<skill>/scripts/``, so the parent is normally the skill
    root. Walk upward as a fallback if the layout differs.
    """
    here = Path(__file__).resolve().parent
    for candidate in (here.parent, *here.parents):
        if (candidate / "SKILL.md").is_file():
            return candidate
    return here.parent


def display_skill_home() -> str:
    """Return a user-friendly ``~/``-shortened path to the skill root."""
    home = get_skill_home()
    try:
        return "~/" + str(home.relative_to(Path.home()))
    except ValueError:
        return str(home)
