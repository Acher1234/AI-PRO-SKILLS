"""Google Workspace thin wrapper around ``common.skill_home.SkillHome``.

Library: ``~/.ai-pro-skills/google-workspace`` (or full-tree install).
Credentials (token / client secret): prefer registered skill dir / workspace.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
_LIB = _SCRIPTS.parent  # google-workspace/
_ROOT = _LIB.parent  # AI-PRO-SKILLS/
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from common.skill_home import SkillHome  # noqa: E402

_home = SkillHome("google-workspace", library_home=_LIB)


def get_skill_home() -> Path:
    """Prefer an installed skill dir that already has credentials; else library."""
    for filename in ("google_token.json", "google_client_secret.json", "SKILL.md"):
        path = _home.credential_path(filename)
        if path.is_file():
            return path.parent
    # Full-tree / library layout: SKILL.md next to scripts parent
    if (_LIB / "SKILL.md").is_file():
        return _LIB
    return _home.get_library_home()


def display_skill_home() -> str:
    from common.skill_home import display_path

    return display_path(get_skill_home())


def env_path() -> Path:
    return _home.env_path()
