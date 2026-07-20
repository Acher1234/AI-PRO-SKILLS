# 🧩 How to code a skill / Comment coder un skill

This guide is for the **standalone** [AI-PRO-SKILLS](https://github.com/Acher1234/AI-PRO-SKILLS.git) repository.  
Ce guide s’applique au dépôt **autonome** AI-PRO-SKILLS.

## 📁 Skill structure

Each skill = **one folder at the repo root**:

```
AI-PRO-SKILLS/
└── mon-skill/
    ├── SKILL.md            ← Agent skill (EN) — slash commands + how to run
    ├── README.md           ← Docs (EN)
    ├── README.fr.md        ← Docs (FR) — or README-FR.md
    ├── dependencies.md     ← System / pip deps
    ├── .gitignore          ← Ignore secrets (config.json, __pycache__)
    ├── config.example.json ← Config template (no secrets)
    └── mon-script.py       ← Executable CLI
```

## 🎯 SKILL.md (required)

Every skill **must** ship a `SKILL.md`. It is the English agent entrypoint: when to use the skill, how to launch the CLI, and slash actions.

### Purpose

- Cursor discovers and invokes the skill via `/skill-name`.
- Actions use: `/{skill-name}_{command}`
  - examples: `/coolify_deploy`, `/zscaler_zia_create-forwarding-rule`
- Nested CLI verbs: `/{skill}_{product}_{action}` (e.g. ZIA under zscaler).

### Required structure

```markdown
---
name: skill-name
description: What it does and when to use it (third person, include trigger terms).
disable-model-invocation: true
---

# skill-name

## When to use
One short paragraph with trigger phrases.

## Working directory
`~/.ai-pro-skills/<skill-dir>` (e.g. `~/.ai-pro-skills/coolify`).

## Credentials (shared code, local secrets)

- **CLI / code** stays in the shared library (`~/.ai-pro-skills/<skill>/`).
- **Secrets** (`.env`, `config.json`, tokens) live next to the *registered* skill or in the
  workspace — use [`common/skill_home.py`](common/skill_home.py):

```python
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common.skill_home import SkillHome

home = SkillHome("my-skill", library_home=Path(__file__).resolve().parent)
env = home.env_path()  # ./.cursor/skills/my-skill/.env or ~/.cursor/skills/…
```

Register = `cp` **only** `SKILL.md`; create `.env` under `$DEST/my-skill/.env`.

| Slash | CLI | Description |
|-------|-----|-------------|
| `/skill-name_command` | `./script.py command …` | … |

## How to run
Steps: `cd ~/.ai-pro-skills/<skill-dir>`, ensure config/env, then run the matching CLI.

## Notes
Config path, activation, safety, etc.
```

### Naming rules

| Rule | Example |
|------|---------|
| `name` in frontmatter = slash prefix | `name: coolify` → `/coolify_*` |
| Lowercase, hyphens OK in skill name | `zscaler`, `coolify` |
| Command segment = CLI subcommand | `/zscaler_zia_add-url` |
| One row per real CLI action | Do not invent aliases without a CLI |
| Body language = **English only** | French stays in `README*.md` |

### Checklist when adding a skill

1. Create the folder + CLI + READMEs + `dependencies.md` + `config.example.json`
2. Write **`SKILL.md`** with full slash-command table
3. Document working dir as `~/.ai-pro-skills/<skill-dir>`
4. After merge: users (or `/ai-pro-skills`) **copy** into `~/.cursor/skills/<skill-name>/SKILL.md`
5. Keep slash list in sync when CLI commands change
6. See root [`SKILL.md`](SKILL.md) for the Cursor install prompt

> Cursor only loads skills from `~/.cursor/skills/` (or `.agents/skills/`, project `.cursor/skills/`).  
> A `SKILL.md` next to the CLI is the source of truth; it **must** also be installed under `~/.cursor/skills/`.

## 📝 README.md / README.fr.md

Each README should cover:
- **Installation**
- **Configuration** (`config.json` example)
- **Usage** (all commands)
- **Filters / options** (if any)
- **States** (if any)
- **Dependencies** → `dependencies.md`
- **Environment** variables

> `SKILL.md` = agent + slash commands (EN).  
> `README*.md` = human docs. Both are required.

## 📦 dependencies.md

```markdown
| Package | Version | Install | Usage |
|---------|---------|---------|-------|
| `python3` | 3.11+ | `apt-get install python3` | Runtime |
```

## 🔐 config.example.json

Template **without secrets** — real values go in `config.json` (gitignored).

```json
{
  "url": "http://...",
  "username": "admin",
  "password": "YOUR_PASSWORD"
}
```

## 🐍 Python script

The script must:
- Be **executable** (`chmod +x`)
- Use a config path env var when possible
- Target **Python 3.11+** (stdlib preferred)
- Use `argparse` with subcommands

```python
#!/usr/bin/env python3
"""Script docstring."""

import argparse
import json
import os
import sys

CONFIG_PATH = os.environ.get("MY_CONFIG_PATH", "config.json")

def load_config():
    ...

def main():
    ...
```

## 🔒 Security

- Never commit `config.json` → `.gitignore`
- Secrets via env vars or files outside the repo (`~/.hermes/...`)
- Prefer a `pre-commit` gitleaks hook when the repo has one

## 🚀 Creation workflow

```bash
# 1. Branch
git checkout -b feat/mon-skill

# 2. Folder + files (include SKILL.md)
mkdir mon-skill
# ...

# 3. Test
./mon-skill/mon-script.py --help

# 4. Commit + push
git add mon-skill/
git commit -m "feat: add mon-skill CLI"
git push -u origin feat/mon-skill

# 5. Open a PR on GitHub
```

After merge, re-run the root install prompt (`/ai-pro-skills`) so Cursor gets the new `SKILL.md`.

---

*Keep skills consistent and maintainable across AI-PRO-SKILLS.*
