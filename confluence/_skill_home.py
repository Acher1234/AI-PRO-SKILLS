"""Confluence thin wrapper around ``common.skill_home.SkillHome``."""

from __future__ import annotations

import sys
from pathlib import Path

_LIB = Path(__file__).resolve().parent
_ROOT = _LIB.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from common.skill_home import SkillHome  # noqa: E402

_home = SkillHome("confluence", library_home=_LIB)

get_library_home = _home.get_library_home
get_skill_home = _home.get_skill_home
display_skill_home = _home.display_skill_home
display_env_path = _home.display_env_path
env_path = _home.env_path
preferred_env_path = _home.preferred_env_path
