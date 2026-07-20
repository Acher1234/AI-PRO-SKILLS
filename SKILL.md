---
name: ai-pro-skills
description: >-
  Install or update AI-PRO-SKILLS into Cursor, Claude, Hermes, or OpenClaw. Clone/pull
  this repo into ~/.ai-pro-skills (shared library), auto-detect the tool via TERMINAL_ENV
  / CLAUDECODE, ask target + scope, then copy (cp) chosen SKILL.md files. Any external git
  skill repo is cloned ONCE into ~/.ai-pro-skills/ext via `install.sh fetch`; each skill
  installs its OWN deps on first run via `install.sh pip init` / `npm init` into a shared
  env (~/.ai-pro-skills/.venv). Use when installing/refreshing pro skills, adding a skill
  from a git URL, sharing a python/npm env across projects, or running /ai-pro-skills.
disable-model-invocation: true
---

# AI-PRO-SKILLS — the pro skill installer (Cursor / Claude / Hermes / OpenClaw)

This skill **is** the installer. It manages a **single shared library and a single
shared Python/npm environment** on the machine, then registers chosen skills into
any tool. Nothing is re-cloned or re-installed per project.

This repository is **standalone** ([Acher1234/AI-PRO-SKILLS](https://github.com/Acher1234/AI-PRO-SKILLS.git)).
It is not the same as [AI-Skills](https://github.com/Acher1234/AI-Skills.git) — same
installer flow, but its shared library lives at `~/.ai-pro-skills`.

> **Targets:** `cursor`, `claude`, `hermes`, `openclaw`.
> **`claude` and `openclaw` are in progress** — their paths (see the
> [Targets table](#targets--scopes)) are working defaults and may still change.

## Core idea — shared library, shared env

Heavy things live **once** under `$AI_SKILLS_HOME` (default `~/.ai-pro-skills`);
each tool only gets the lightweight `SKILL.md`.

```
~/.ai-pro-skills/        shared library root (this repo, or $AI_SKILLS_HOME)
├── install.sh           this installer's helper script
├── common/              shared helpers — skill_home (lib shared + .env per workspace)
├── ext/<repo>/          external git skills, cloned ONCE (shared)
├── .venv/               shared Python venv — every python skill reuses it
└── <skills>/            coolify, zscaler, reddit, jira, …

                         node deps via `./install.sh npm init` (shared skill dir)

        │ register = cp ONLY SKILL.md ; put .env next to the registered skill ↓
~/.cursor/skills/<name>/{SKILL.md,.env}   (or ./.cursor/skills/<name>/ per project)
```

**Hybrid model:** CLI code is **shared**; credentials (`.env` / tokens) are **per workspace**,
resolved by [`common/skill_home.py`](common/skill_home.py) (`SkillHome("reddit")`, `SkillHome("jira")`, …).

## Hybrid model — shared CLI, local secrets (`common/skill_home`)

Do **not** put secrets in `~/.ai-pro-skills/<skill>/` (that would force one account for every
project). Do **not** copy the full skill tree into Cursor/Hermes for Python CLIs that follow
this pattern (exception: vendored full-tree skills like `google-workspace` / `powerpoint`).

| Layer | Location | Shared? |
|-------|----------|---------|
| CLI / Python code | `~/.ai-pro-skills/<skill>/` | **Yes** — one copy on the machine |
| Python deps | `~/.ai-pro-skills/.venv` | **Yes** |
| Registered skill | `$DEST/<skill>/SKILL.md` only | Lightweight discovery copy |
| Credentials | `$DEST/<skill>/.env` (preferred) | **No** — per workspace / profile |

**Credential resolution** (`SkillHome("<name>").env_path()`), in order:

1. `<NAME>_ENV_PATH` override (e.g. `REDDIT_ENV_PATH`)
2. Project: `./.cursor/skills/<name>/.env` (also `.claude` / `.openclaw` / Hermes)
3. Workspace root: `./.env`
4. Global: `~/.cursor/skills/<name>/.env` (and Hermes / Claude / OpenClaw equivalents)
5. Tool-level fallback: `~/.cursor/.env`, `$HERMES_HOME/.env`, …

**Authoring a skill that uses it:**

```python
# <skill>/_skill_home.py — thin wrapper
from pathlib import Path
import sys
_LIB = Path(__file__).resolve().parent
sys.path.insert(0, str(_LIB.parent))
from common.skill_home import SkillHome
_home = SkillHome("my-skill", library_home=_LIB)
env_path = _home.env_path
```

```bash
# Register (Cursor project = different Reddit/Jira per repo)
mkdir -p ./.cursor/skills/my-skill
cp ~/.ai-pro-skills/my-skill/SKILL.md ./.cursor/skills/my-skill/SKILL.md
cp ~/.ai-pro-skills/my-skill/.env.example ./.cursor/skills/my-skill/.env
# edit ./.cursor/skills/my-skill/.env

# Run from the shared library
cd ~/.ai-pro-skills/my-skill
~/.ai-pro-skills/.venv/bin/python cli.py test
```

Full-tree exceptions (`google-workspace`, `powerpoint`) still `cp -R` when scripts must live
next to the installed tree; prefer `SkillHome` for new Python skills.

Agent authors: Cursor rule [`.cursor/rules/ai-pro-skills-hybrid.mdc`](.cursor/rules/ai-pro-skills-hybrid.mdc)
encodes the same conventions when editing skills in this repo.
Copy-paste prompt for agents: [`common/PROMPT.md`](common/PROMPT.md).

## Helper script — [`install.sh`](install.sh) (3 commands)

`~/.ai-pro-skills/install.sh` has **exactly three** commands. They only manage the
**shared** cache/env — nothing per project:

```bash
./install.sh fetch <git-url> [name]   # clone/pull an external skill repo → ~/.ai-pro-skills/ext/<name>
./install.sh pip init [dir]           # create/reuse the shared venv, install <dir> deps into it
./install.sh npm init [dir]           # install <dir> node deps (shared skill dir)
```

- **Registering** a skill into a tool is a plain `cp` (see the [Copy map](#copy-map-reference)).
- **Dependencies are each skill's job.** A skill calls `install.sh pip init .` /
  `install.sh npm init .` from its own folder on **first run** — installed once into
  the shared venv (`~/.ai-pro-skills/.venv`), reused across projects. The installer never
  bulk-installs anything.

## Targets & scopes

| Tool | Scope | Skills directory |
|------|-------|------------------|
| **cursor** | `global` | `~/.cursor/skills/<name>/` |
| **cursor** | `project` | `./.cursor/skills/<name>/` |
| **claude** | `global` | `~/.claude/skills/<name>/` *(WIP)* |
| **claude** | `project` | `./.claude/skills/<name>/` *(WIP)* |
| **hermes** | `all` | `~/.hermes/skills/<name>/` |
| **hermes** | `profile` | `${HERMES_HOME}/skills/<name>/` |
| **openclaw** | `global` | `~/.openclaw/skills/<name>/` *(WIP)* |
| **openclaw** | `project` | `./.openclaw/skills/<name>/` *(WIP)* |

## Critical — ask the user first

**Do not copy every skill blindly.** After clone/pull, resolve the tool (auto-detect
first), then ask in this order:

### 0) Auto-detect the tool

Check the environment:

- **`TERMINAL_ENV` set (non-empty)** → **Hermes**. Skip to the Hermes profile scope (step 2).
- **`CLAUDECODE`/`CLAUDE_CODE` set, or `~/.claude` exists** (and no `TERMINAL_ENV`) → likely **Claude**.
- **Otherwise** → assume **Cursor**.
- **OpenClaw** is chosen explicitly (WIP). Only fall back to the tool question (step 1)
  if detection is ambiguous or the user wants **several** tools.

### 1) Target tool (only if not auto-detected)

> Install skills for **Cursor**, **Claude**, **Hermes**, and/or **OpenClaw**? (one or several)

### 2) Scope

- **Cursor / Claude / OpenClaw** → **global** (`~/.<tool>/skills`) or **this project** (`./.<tool>/skills`).
- **Hermes** → **all profiles** (`~/.hermes/skills`) or **this profile** (`$HERMES_HOME/skills`; resolve `HERMES_HOME`, ask if unset).

### 3) Which skills

Ask for any of:
- **built-in** pro skills (catalog below),
- an **external git URL** (any skill repo), or
- a **local path** to a skill folder.

Always also install the meta skill `ai-pro-skills` (this file) into every chosen target.

### Skills catalog (show this to the user)

| # | Name | Folder | What it does |
|---|------|--------|--------------|
| 1 | `coolify` | `coolify/` | Coolify deploy / status / restart |
| 2 | `zscaler` | `zscaler/` | Zscaler ZPA / ZIA / ZIdentity |
| 3 | `agent-browser` | `agent-browser/` (stub + npm) | Browser automation CLI — `npm i -g agent-browser` ([upstream](https://github.com/vercel-labs/agent-browser)) |
| 4 | `sf` | `SF/` | Salesforce skills from [forcedotcom/sf-skills](https://github.com/forcedotcom/sf-skills.git) → `~/.ai-skills/sf-skills` |
| 5 | `google-workspace` | `google-workspace/` (vendored) | Gmail / Calendar / Drive / Docs / Sheets |
| 6 | `powerpoint` | `powerpoint/` (vendored) | Create / edit .pptx decks |
| 7 | `jira` | `jira/` | **All** JIRA Assistant skills + `jira-as` CLI — run `/jira` |
| 8 | `reddit` | `reddit/` | Reddit API via PRAW — shared CLI; `.env` per workspace / install |

**External** — any git URL (cloned into `~/.ai-pro-skills/ext/<name>`).

## Flow (do this)

```
# 0) Shared library — clone/pull into ~/.ai-pro-skills (rename to .ai-pro-skills)
If ~/.ai-pro-skills exists:  cd ~/.ai-pro-skills && git pull
Else:                        git clone https://github.com/Acher1234/AI-PRO-SKILLS.git ~/.ai-pro-skills

# 1) Detect tool: $TERMINAL_ENV set → Hermes; $CLAUDECODE or ~/.claude → Claude; else Cursor.
#    OpenClaw only when explicitly asked. Ask if ambiguous / several tools wanted.
# 2) Ask scope (see table). For Hermes-profile, resolve HERMES_HOME.
# 3) Ask what to install: built-in name(s), external git URL, or local path. Do not copy all by default.

# 4a) EXTERNAL git skill → fetch it into the shared cache (clone once):
SRC=$(cd ~/.ai-pro-skills && ./install.sh fetch <git-url> [name])
# 4b) BUILT-IN or LOCAL skill: SRC is its folder under ~/.ai-pro-skills/…

# 5) Register = copy ONLY the SKILL.md into each chosen tool/scope (+ always ai-pro-skills).
#    Resolve DEST from the Targets table, then (see Copy map):
mkdir -p "$DEST/<name>" && cp "$SRC/SKILL.md" "$DEST/<name>/SKILL.md"
mkdir -p "$DEST/ai-pro-skills" && cp ~/.ai-pro-skills/SKILL.md "$DEST/ai-pro-skills/SKILL.md"

# 6) Reload Cursor / Claude / OpenClaw, or reload the Hermes agent.
# NOTE: the installer does NOT install deps. Each skill runs `./install.sh pip init .`
#       (or `npm init .`) itself on first run → shared venv ~/.ai-pro-skills/.venv.
```

## Examples

```bash
cd ~/.ai-pro-skills

# Built-in → Cursor (global): register = cp the SKILL.md
mkdir -p ~/.cursor/skills/{coolify,ai-pro-skills}
cp ~/.ai-pro-skills/coolify/SKILL.md ~/.cursor/skills/coolify/SKILL.md
cp ~/.ai-pro-skills/SKILL.md         ~/.cursor/skills/ai-pro-skills/SKILL.md

# zscaler → Hermes (this profile)
mkdir -p "$HERMES_HOME/skills/zscaler"
cp ~/.ai-pro-skills/zscaler/SKILL.md "$HERMES_HOME/skills/zscaler/SKILL.md"

# agent-browser → cp the stub into Claude (the skill installs its own CLI on first run)
mkdir -p ~/.claude/skills/agent-browser
cp ~/.ai-pro-skills/agent-browser/SKILL.md ~/.claude/skills/agent-browser/SKILL.md

# google-workspace / powerpoint → copy the FULL folder (Hermes → productivity/)
cp -R ~/.ai-pro-skills/google-workspace ~/.cursor/skills/google-workspace

# reddit → shared CLI; register SKILL.md only; put .env next to the registered skill
mkdir -p ~/.cursor/skills/reddit
cp ~/.ai-pro-skills/reddit/SKILL.md ~/.cursor/skills/reddit/SKILL.md
cp ~/.ai-pro-skills/reddit/.env.example ~/.cursor/skills/reddit/.env   # edit tokens
# (project scope: same under ./.cursor/skills/reddit/ for a per-workspace account)

# External git skill → OpenClaw (global): fetch once, then cp the SKILL.md
SRC=$(./install.sh fetch https://github.com/some/pro-skill.git pro-skill)
mkdir -p ~/.openclaw/skills/pro-skill
cp "$SRC/SKILL.md" ~/.openclaw/skills/pro-skill/SKILL.md
./install.sh pip init "$SRC"     # the skill installs ITS OWN deps into the shared venv
```

## Agent checklist

1. Clone/pull `~/.ai-pro-skills`.
2. Detect tool (`$TERMINAL_ENV` → Hermes; `$CLAUDECODE`/`~/.claude` → Claude; else Cursor). Ask if ambiguous / several.
3. Ask scope; resolve `HERMES_HOME` for Hermes-profile.
4. Ask what to install (built-in / external git URL / local path). Don't copy all by default.
5. External repo → `./install.sh fetch <url> [name]` (clone once into the shared cache).
6. **Register = `cp` the `SKILL.md`** into `$DEST/<name>/` for each chosen target (see Copy map); always also copy `ai-pro-skills`.
7. **Dependencies are each skill's responsibility** — the skill runs `./install.sh pip init .` / `npm init .` on first run into the shared venv (`~/.ai-pro-skills/.venv`), once per machine. The installer never bulk-installs deps.
8. Special cases (each handled by the skill itself, per its own `SKILL.md`):
   - `agent-browser` → the skill runs `npm i -g agent-browser && agent-browser install`, then `agent-browser skills get core`.
   - `sf` → run `/sf` (syncs into `~/.ai-skills/sf-skills`).
   - `jira` → run `/jira` (fetches all skills + `jira-as`).
   - `google-workspace` / `powerpoint` → copy the **full folder**; Hermes → `$DEST/productivity/<skill>/`.
9. Remind: reload the tool(s).

## Copy map (reference)

Pick `DEST` from the [Targets table](#targets--scopes): `~/.cursor/skills`, `./.cursor/skills`,
`~/.claude/skills`, `./.claude/skills`, `~/.hermes/skills`, `$HERMES_HOME/skills`,
`~/.openclaw/skills`, or `./.openclaw/skills`. Then `mkdir -p "$DEST/<name>"` and `cp`:

| Source (`~/.ai-pro-skills/…`) | Target |
|-------------------------------|--------|
| `SKILL.md` | `$DEST/ai-pro-skills/SKILL.md` |
| `coolify/SKILL.md` | `$DEST/coolify/SKILL.md` |
| `zscaler/SKILL.md` | `$DEST/zscaler/SKILL.md` |
| `agent-browser/SKILL.md` | `$DEST/agent-browser/SKILL.md` |
| `SF/SKILL.md` | `$DEST/sf/SKILL.md` |
| `jira/SKILL.md` | `$DEST/jira/SKILL.md` (then run `/jira`) |
| `google-workspace/` (full tree) | Cursor/Claude/OpenClaw: `$DEST/google-workspace/` · Hermes: `$DEST/productivity/google-workspace/` |
| `powerpoint/` (full tree) | Cursor/Claude/OpenClaw: `$DEST/powerpoint/` · Hermes: `$DEST/productivity/powerpoint/` |
| `reddit/SKILL.md` | `$DEST/reddit/SKILL.md` (+ create `$DEST/reddit/.env` from `.env.example`; CLI stays in `~/.ai-pro-skills/reddit`) |
| `ext/<name>/SKILL.md` | `$DEST/<name>/SKILL.md` |

## After install

- CLI working dirs stay under `~/.ai-pro-skills/<skill-dir>` (or `~/.ai-pro-skills/ext/<name>`).
- Python skills should use the shared interpreter `~/.ai-pro-skills/.venv/bin/python`.
- For **agent-browser**, the binary is global (`agent-browser …`); the local folder is only the skill stub.
- For **sf**, Salesforce skill trees live in `~/.ai-skills/sf-skills/skills/{skills_dir}`.
- For **reddit** / similar skills: CLI in `~/.ai-pro-skills/<skill>`; `.env` per install via
  `common/skill_home.py` → `$DEST/<skill>/.env`.
- Re-run `/ai-pro-skills` anytime to **pull + ask targets/skills again + re-register**.

## Notes

- Override the shared library location with `AI_SKILLS_HOME` (default `~/.ai-pro-skills`).
- Never write into `~/.cursor/skills-cursor/` (Cursor built-ins only).
- Register with `cp` (copy, not move). Prefer **per-skill** credentials next to the registered
  skill (`$DEST/<name>/.env`) so each workspace can differ; tool-level `.env`
  (`~/.cursor/.env`, `$HERMES_HOME/.env`, …) remains a fallback. Use
  [`common/skill_home.py`](common/skill_home.py) from Python CLIs.
- Claude / OpenClaw support is **in progress** — adjust their paths in the Targets table if needed.
- Repo: [Acher1234/AI-PRO-SKILLS](https://github.com/Acher1234/AI-PRO-SKILLS.git)
- agent-browser CLI: [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) via npm (this repo only keeps the stub)
- Vendored skills: [google-workspace](https://github.com/NousResearch/hermes-agent/tree/main/skills/productivity/google-workspace), [powerpoint](https://github.com/NousResearch/hermes-agent/tree/main/skills/productivity/powerpoint) (see each `ORIGIN.md`)
