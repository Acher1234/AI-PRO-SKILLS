---
name: jira
description: >-
  Install or update the JIRA Assistant skills from grandcamel/JIRA-Assistant-Skills.
  Downloads ALL skills (every skills/*/SKILL.md) into a chosen destination (Cursor
  global/project or Hermes global/profile, auto-detected via TERMINAL_ENV), installs
  the jira-as CLI, and sets up Jira credentials in a .env. Use when the user wants
  Jira skills, mentions Jira issues/sprints/boards/worklogs, or runs /jira.
disable-model-invocation: true
---

# Jira — JIRA Assistant Skills installer (Cursor or Hermes)

Meta-skill that downloads **all** the JIRA Assistant skills from
[grandcamel/JIRA-Assistant-Skills](https://github.com/grandcamel/JIRA-Assistant-Skills.git)
and installs every `skills/*/SKILL.md` into the user's chosen Cursor or Hermes skills
directory, installs the `jira-as` CLI, and configures Jira credentials.

## When to use

- User asks to install Jira skills, or invokes `/jira`.
- User mentions Jira issues, sprints, boards, worklogs, comments, links, JSM, bulk ops, etc.
- **Every time this skill is recalled:** re-propose an update (pull + re-copy all skills) — do not assume the local copy is current.

## What gets installed (ALL skills)

Install **every** skill folder under `skills/` (do not ask which — install them all):

| Skill | Purpose |
|-------|---------|
| `jira-assistant` | Meta-skill router (routes to the right skill) |
| `jira-issue` | Issue CRUD |
| `jira-lifecycle` | Workflow transitions |
| `jira-search` | JQL & filters |
| `jira-collaborate` | Comments & watchers |
| `jira-agile` | Sprints & epics |
| `jira-relationships` | Issue linking |
| `jira-time` | Time tracking |
| `jira-jsm` | Service desk (JSM) |
| `jira-bulk` | Bulk operations |
| `jira-dev` | Git integration |
| `jira-fields` | Field discovery |
| `jira-ops` | Cache & utilities |
| `jira-admin` | Project admin |

> The list above is indicative — always enumerate the **actual** `skills/*/` folders after clone/pull and copy every one of them (the repo may add or rename skills).

## Critical — ask the user first (destination only)

**Install all skills**, but ask **where** to install. Auto-detect the platform first.

### 0) Auto-detect platform (Cursor vs Hermes)

Check `TERMINAL_ENV` (e.g. `echo "$TERMINAL_ENV"`):

- **`TERMINAL_ENV` set (non-empty)** → **Hermes**. Skip the platform question, go to profile scope.
- **`TERMINAL_ENV` empty/unset** → **Cursor**. Skip the question, go to Cursor scope.
- Only ask the platform question if ambiguous or the user explicitly wants **both**.

### 1) Destination

> Install the JIRA Assistant skills to **Cursor** or **Hermes**?

| Target | Skills directory | Env file for credentials |
|--------|------------------|--------------------------|
| **Cursor — global** | `~/.cursor/skills/<skill>/` | Prefer `~/.cursor/skills/jira/.env` (or `~/.cursor/.env`) |
| **Cursor — this project (perso)** | `./.cursor/skills/<skill>/` | Prefer `./.cursor/skills/jira/.env` (or `./.env`) |
| **Hermes — all profiles** | `~/.hermes/skills/<skill>/` | Prefer `~/.hermes/skills/jira/.env` (or `~/.hermes/.env`) |
| **Hermes — this profile only** | `${HERMES_HOME}/skills/<skill>/` | Prefer `${HERMES_HOME}/skills/jira/.env` (or `$HERMES_HOME/.env`) |

Per-workspace **skill-scoped** `.env` (recommended for multiple Jira sites) follows the shared helper
[`common/skill_home.py`](../common/skill_home.py): register `SKILL.md` only, keep `jira-as` in the
shared venv, put secrets next to the registered skill so each project can differ.

Tool-level `.env` (`~/.cursor/.env`, `./.env`, …) remains supported as a fallback (same `JIRA_*` keys).


### 2) Credentials (.env)

After copying the skills, set up Jira credentials so the `jira-as` CLI can authenticate.

- **Preferred (per workspace):** create `$DEST/jira/.env` (e.g. `./.cursor/skills/jira/.env` or
  `~/.cursor/skills/jira/.env`) with:

```bash
export JIRA_API_TOKEN="your-token"
export JIRA_EMAIL="you@company.com"
export JIRA_SITE_URL="https://company.atlassian.net"
```

Also copy the meta `jira/SKILL.md` into `$DEST/jira/` if missing, so the folder is the credential
anchor. Resolve path with `common.skill_home.SkillHome("jira")` when wrapping in Python.

- **Fallback (tool-level):** Cursor → `~/.cursor/.env` or `./.env`; Hermes → append the same three
  `export` lines to `$HERMES_HOME/.env` / `~/.hermes/.env` if not already present.


Rules:
- Never overwrite an existing real token — if the var is already set in the file, leave it. Only add missing lines (or create the file if absent).
- Remind the user to replace the placeholder values and to `source` the `.env` (or add it to their shell rc) so the vars are available to the `jira-as` CLI.
- Token page: <https://id.atlassian.com/manage-profile/security/api-tokens>.

## Prompt (do this)

```
Source: https://github.com/grandcamel/JIRA-Assistant-Skills.git
Local cache: ~/.ai-pro-skills/jira/JIRA-Assistant-Skills

If the cache exists: cd it and `git pull --ff-only`. Else `git clone --depth 1 <repo> <cache>`.

IMPORTANT — every time /jira is invoked:
0. Detect platform: check $TERMINAL_ENV. Set (non-empty) → Hermes; empty/unset → Cursor.
   Only ask Cursor vs Hermes if ambiguous or the user wants both.
1. Clone/pull the repo first.
2. Ask destination:
     Cursor: global (~/.cursor/skills) or this project/perso (./.cursor/skills)
     Hermes: all profiles (~/.hermes/skills) or this profile ($HERMES_HOME/skills)
3. Install ALL skills: copy EVERY skills/*/ folder from the repo into the destination,
   and PREPEND a shared-env header at the TOP of every installed SKILL.md (after its
   front-matter) stating: env is shared (venv ~/.ai-pro-skills/.venv, jira-as at
   ~/.ai-pro-skills/.venv/bin/jira-as) and where the scripts live (cache
   ~/.ai-pro-skills/jira/JIRA-Assistant-Skills). See the loop in "Commands".
4. Install the CLI into the SHARED venv (~/.ai-pro-skills/.venv):
     ~/.ai-pro-skills/install.sh pip init <cache>   # creates the shared venv + installs the repo (editable) if it ships a package
     ~/.ai-pro-skills/.venv/bin/pip install jira-as # or the published CLI, into the same shared venv
   (do not create a per-skill venv; the jira-as binary lands in ~/.ai-pro-skills/.venv/bin/)
5. Credentials (.env):
     Cursor → create the .env (see destination table) with the 3 exports.
     Hermes → append the 3 exports to the profile .env ($HERMES_HOME/.env or ~/.hermes/.env).
   Only add missing lines; never overwrite an existing token. Remind to edit + source it.

Reload Cursor if Cursor was the target. For Hermes, reload/restart the agent if needed.
```

## Commands

```bash
# 1) Clone / update
REPO=https://github.com/grandcamel/JIRA-Assistant-Skills.git
CACHE=~/.ai-pro-skills/jira/JIRA-Assistant-Skills
mkdir -p ~/.ai-pro-skills/jira
if [ -d "$CACHE/.git" ]; then
  git -C "$CACHE" pull --ff-only
else
  git clone --depth 1 "$REPO" "$CACHE"
fi

# 2) Pick ONE destination (chosen by the user)
DEST=~/.cursor/skills          # Cursor global
# DEST=./.cursor/skills        # Cursor this project (perso)
# DEST=~/.hermes/skills        # Hermes all profiles
# DEST="$HERMES_HOME/skills"   # Hermes this profile

# 3) Install ALL skills (every skills/*/ folder) + prepend a shared-env header to each SKILL.md
NOTE='> **Installed via /jira — shared environment.** Runs through the shared venv `~/.ai-pro-skills/.venv`; the `jira-as` CLI is at `~/.ai-pro-skills/.venv/bin/jira-as` (or `source ~/.ai-pro-skills/.venv/bin/activate`). Scripts / repo cache: `~/.ai-pro-skills/jira/JIRA-Assistant-Skills`. Credentials come from the tool `.env`.'
for d in "$CACHE"/skills/*/; do
  name=$(basename "$d")
  mkdir -p "$DEST/$name"
  cp -R "$d." "$DEST/$name/"
  f="$DEST/$name/SKILL.md"
  [ -f "$f" ] || continue
  # insert NOTE just after the YAML front-matter (or at the very top if none), once
  awk -v note="$NOTE" '
    NR==1 && $0=="---" {print; fm=1; next}
    fm && $0=="---" && !done {print; print ""; print note; done=1; next}
    {print}
  ' "$f" > "$f.tmp"
  grep -qF "$NOTE" "$f.tmp" || { printf "%s\n\n" "$NOTE" | cat - "$f" > "$f.tmp"; }
  mv "$f.tmp" "$f"
done

# 4) Install the jira-as CLI into the SHARED venv (~/.ai-pro-skills/.venv, not a per-skill venv)
~/.ai-pro-skills/install.sh pip init "$CACHE"    # ensures the shared venv + installs the repo (editable) if it's a package
~/.ai-pro-skills/.venv/bin/pip install jira-as   # or the published CLI, into the same shared venv
# jira-as binary is now at ~/.ai-pro-skills/.venv/bin/jira-as

# 5) Credentials .env (choose the matching ENV_FILE for the destination)
ENV_FILE=~/.cursor/.env         # Cursor global
# ENV_FILE=./.env               # Cursor this project (perso)
# ENV_FILE=~/.hermes/.env       # Hermes all profiles
# ENV_FILE="$HERMES_HOME/.env"  # Hermes this profile
touch "$ENV_FILE"
grep -q '^export JIRA_API_TOKEN=' "$ENV_FILE" || echo 'export JIRA_API_TOKEN="your-token"' >> "$ENV_FILE"
grep -q '^export JIRA_EMAIL='     "$ENV_FILE" || echo 'export JIRA_EMAIL="you@company.com"' >> "$ENV_FILE"
grep -q '^export JIRA_SITE_URL='  "$ENV_FILE" || echo 'export JIRA_SITE_URL="https://company.atlassian.net"' >> "$ENV_FILE"
echo "Edit $ENV_FILE with your real values, then: source $ENV_FILE"
```

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `JIRA_SITE_URL` | Yes | Jira base URL (e.g. `https://company.atlassian.net`) |
| `JIRA_EMAIL` | Yes | Atlassian account email |
| `JIRA_API_TOKEN` | Yes | Atlassian API token ([generate](https://id.atlassian.com/manage-profile/security/api-tokens)) |
| `JIRA_PROFILE` | No | Config profile for multi-instance (defaults to production) |

## Quick check

Use the shared-venv binary (`~/.ai-pro-skills/.venv/bin/jira-as`), or `source ~/.ai-pro-skills/.venv/bin/activate` first:

```bash
~/.ai-pro-skills/.venv/bin/jira-as --version
~/.ai-pro-skills/.venv/bin/jira-as issue get PROJ-123
~/.ai-pro-skills/.venv/bin/jira-as search query "project = PROJ AND status = Open"
```

## Agent checklist

1. Clone/pull `~/.ai-pro-skills/jira/JIRA-Assistant-Skills`.
2. Detect platform via `$TERMINAL_ENV` (set → Hermes, unset → Cursor). Only ask if ambiguous.
3. Ask destination — Cursor global vs project (perso), or Hermes all vs this profile (resolve `HERMES_HOME`).
4. Install **all** skills: copy every `skills/*/` folder into the destination, and **prepend a shared-env header** to the top of each installed `SKILL.md` (shared venv `~/.ai-pro-skills/.venv`, `jira-as` binary, scripts cache path) — see the loop in "Commands".
5. Install the CLI into the **shared** venv: `~/.ai-pro-skills/install.sh pip init <cache>` then `~/.ai-pro-skills/.venv/bin/pip install jira-as` (binary at `~/.ai-pro-skills/.venv/bin/jira-as`).
6. Credentials: Cursor → **create** the destination `.env`; Hermes → **append** to the profile `.env`. Only add missing `export` lines; never overwrite a real token.
7. Remind the user to edit the placeholders and `source` the `.env`.
8. Tell the user to reload Cursor and/or Hermes.

## Notes

- Cache / working copy: `~/.ai-pro-skills/jira/JIRA-Assistant-Skills` (full clone; source of the `jira-as` editable install).
- v4 is CLI-only: skills invoke the global `jira-as` CLI, so credentials just need to be in the environment (via the `.env`).
- Never commit real tokens. Keep the `.env` out of version control.
- Upstream: [grandcamel/JIRA-Assistant-Skills](https://github.com/grandcamel/JIRA-Assistant-Skills.git) (MIT).
