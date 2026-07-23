"""Fathom thin wrapper around ``common.skill_home.SkillHome``.

Resolves the shared library dir and the per-workspace ``.env``
(``FATHOM_API_KEY``) depending on where the skill is registered
(Cursor project / Cursor global / Hermes profile / AI-PRO-SKILLS clone).

Run directly to print the resolved ``.env`` path::

    python3 scripts/_skill_home.py
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
_LIB = _SCRIPTS.parent  # fathom/
_ROOT = _LIB.parent      # AI-PRO-SKILLS/
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from common.skill_home import SkillHome  # noqa: E402

_home = SkillHome("fathom", library_home=_LIB)

get_library_home = _home.get_library_home
get_skill_home = _home.get_skill_home
display_skill_home = _home.display_skill_home
display_env_path = _home.display_env_path
env_path = _home.env_path
preferred_env_path = _home.preferred_env_path


if __name__ == "__main__":
    print(env_path())
