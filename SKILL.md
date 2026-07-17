---
name: ai-pro-skills
description: >-
  Install or update AI-PRO-SKILLS: clone/pull into ~/.ai-pro-skills, ask Cursor
  vs Hermes target (and Hermes profile vs all), list skills (coolify, zscaler,
  agent-browser, sf, google-workspace, powerpoint), then copy chosen SKILL.md files.
  Use when installing pro skills for Cursor or Hermes, or pasting the install
  prompt from the README.
disable-model-invocation: true
---

# AI-PRO-SKILLS — install prompt (Cursor or Hermes)

Follow this prompt when installing or refreshing **pro** skills.

This repository is **standalone** ([Acher1234/AI-PRO-SKILLS](https://github.com/Acher1234/AI-PRO-SKILLS.git)). It is not the same as [AI-Skills](https://github.com/Acher1234/AI-Skills.git).

## Critical — ask the user first

**Do not copy every skill blindly.** After clone/pull, ask in this order:

### 1) Target platform

> Install skills for **Cursor**, **Hermes**, or **both**?

| Target | Skills directory |
|--------|------------------|
| **Cursor** | `~/.cursor/skills/<skill-name>/SKILL.md` |
| **Hermes — all profiles** | `~/.hermes/skills/<skill-name>/SKILL.md` |
| **Hermes — this profile only** | `${HERMES_HOME}/skills/<skill-name>/SKILL.md` |

### 2) If Hermes (or both): profile scope

> For Hermes, install for **all profiles** (`~/.hermes/skills/`) or **this profile only** (`$HERMES_HOME/skills/`)?

- If **this profile**: require `HERMES_HOME` to be set; if unset, ask for the profile path before copying.
- If **all**: use `~/.hermes/skills/` (create if missing).

### 3) Which skills

**List all available skills** (including stub `agent-browser`, meta `sf`, and vendored `google-workspace`, `powerpoint`), then ask which to install.

Accept: `all`, `coolify`, `zscaler`, `agent-browser`, `sf`, `google-workspace`, `powerpoint`, `1 and 3`, etc.

Always also install the meta skill `ai-pro-skills` (this file) into every chosen target.

### Skills catalog (show this to the user)

| # | Name | Folder | What it does |
|---|------|--------|--------------|
| 1 | `coolify` | `coolify/` | Coolify deploy / status / restart |
| 2 | `zscaler` | `zscaler/` | Zscaler ZPA / ZIA / ZIdentity |
| 3 | `agent-browser` | `agent-browser/` (stub + npm) | Browser automation CLI — install via `npm i -g agent-browser` ([upstream](https://github.com/vercel-labs/agent-browser)) |
| 4 | `sf` | `SF/` | Install/update Salesforce skills from [forcedotcom/sf-skills](https://github.com/forcedotcom/sf-skills.git) → `~/.ai-skills/sf-skills` |
| 5 | `google-workspace` | `google-workspace/` (vendored) | Gmail / Calendar / Drive / Docs / Sheets — from [hermes-agent](https://github.com/NousResearch/hermes-agent/tree/main/skills/productivity/google-workspace) |
| 6 | `powerpoint` | `powerpoint/` (vendored) | Create / edit .pptx decks — from [hermes-agent](https://github.com/NousResearch/hermes-agent/tree/main/skills/productivity/powerpoint) |

Always also install: `ai-pro-skills` ← this file (`SKILL.md` at repo root).

Example questions:

> 1. Target: **Cursor** / **Hermes** / **both**?  
> 2. If Hermes: **all profiles** (`~/.hermes/skills`) or **this profile** (`$HERMES_HOME/skills`)?  
> 3. Skills: **coolify**, **zscaler**, **agent-browser**, **sf**, **google-workspace**, **powerpoint** — which? (`all` / names / numbers)

## Prompt (do this)

```
Take the project at url: https://github.com/Acher1234/AI-PRO-SKILLS.git
Install it on the computer under ~ but rename the folder to .ai-pro-skills

If ~/.ai-pro-skills already exists:
  - cd ~/.ai-pro-skills
  - git pull
Else:
  - git clone https://github.com/Acher1234/AI-PRO-SKILLS.git ~/.ai-pro-skills

IMPORTANT:
1. Ask Cursor vs Hermes vs both.
2. If Hermes: ask all profiles (~/.hermes/skills) vs this profile ($HERMES_HOME/skills).
3. List every skill (coolify, zscaler, agent-browser, sf, google-workspace, powerpoint) and ask which to install.
Do not copy all by default.

Then copy ONLY the chosen skills into EACH selected destination:
  Cursor:  ~/.cursor/skills/<skill-name>/SKILL.md
  Hermes all:     ~/.hermes/skills/<skill-name>/SKILL.md
  Hermes profile: $HERMES_HOME/skills/<skill-name>/SKILL.md

Special — google-workspace / powerpoint (copy full tree, not only SKILL.md):
  Cursor:  $DEST/<skill>/   ← entire folder
  Hermes:  $DEST/productivity/<skill>/  ← same tree (matches upstream paths)

Always copy the root install skill (ai-pro-skills) into each chosen destination.

Reload Cursor if Cursor was a target. For Hermes, restart/reload the agent if needed.
```

## Agent checklist

1. Clone/pull `~/.ai-pro-skills`.
2. Ask **Cursor / Hermes / both**.
3. If Hermes: ask **all** vs **this profile**; resolve `HERMES_HOME` if needed.
4. List skills and ask which to install.
5. Copy `ai-pro-skills` + selected skills into every chosen destination root.
6. If `agent-browser` selected → remind `npm i -g agent-browser && agent-browser install`, then `agent-browser skills get core`.
7. If `sf` selected → copy `SF/SKILL.md`, then remind to run `/sf` to sync [forcedotcom/sf-skills](https://github.com/forcedotcom/sf-skills.git) into `~/.ai-skills/sf-skills`.
8. If `google-workspace` or `powerpoint` selected → copy full folder; for google-workspace remind OAuth via `scripts/setup.py`.
9. Tell the user to reload Cursor and/or Hermes.

## Copy map (reference)

Let `DEST` be one of:
- `~/.cursor/skills`
- `~/.hermes/skills`
- `$HERMES_HOME/skills`

| Source (`~/.ai-pro-skills/…`) | Target |
|-------------------------------|--------|
| `SKILL.md` | `$DEST/ai-pro-skills/SKILL.md` |
| `coolify/SKILL.md` | `$DEST/coolify/SKILL.md` |
| `zscaler/SKILL.md` | `$DEST/zscaler/SKILL.md` |
| `agent-browser/SKILL.md` | `$DEST/agent-browser/SKILL.md` |
| `SF/SKILL.md` | `$DEST/sf/SKILL.md` |
| `google-workspace/` (full tree) | Cursor: `$DEST/google-workspace/` · Hermes: `$DEST/productivity/google-workspace/` |
| `powerpoint/` (full tree) | Cursor: `$DEST/powerpoint/` · Hermes: `$DEST/productivity/powerpoint/` |

```bash
# Example: Cursor + coolify
mkdir -p ~/.cursor/skills/{ai-pro-skills,coolify}
cp ~/.ai-pro-skills/SKILL.md ~/.cursor/skills/ai-pro-skills/SKILL.md
cp ~/.ai-pro-skills/coolify/SKILL.md ~/.cursor/skills/coolify/SKILL.md

# Example: Hermes this profile + zscaler
mkdir -p "$HERMES_HOME/skills/{ai-pro-skills,zscaler}"
cp ~/.ai-pro-skills/SKILL.md "$HERMES_HOME/skills/ai-pro-skills/SKILL.md"
cp ~/.ai-pro-skills/zscaler/SKILL.md "$HERMES_HOME/skills/zscaler/SKILL.md"

# Example: google-workspace / powerpoint (full tree)
# Cursor:
cp -R ~/.ai-pro-skills/google-workspace ~/.cursor/skills/google-workspace
cp -R ~/.ai-pro-skills/powerpoint ~/.cursor/skills/powerpoint
# Hermes:
mkdir -p "$HERMES_HOME/skills/productivity"
cp -R ~/.ai-pro-skills/google-workspace "$HERMES_HOME/skills/productivity/google-workspace"
cp -R ~/.ai-pro-skills/powerpoint "$HERMES_HOME/skills/productivity/powerpoint"
```

## After install

- CLI working dirs: `~/.ai-pro-skills/coolify`, `~/.ai-pro-skills/zscaler`, `~/.ai-pro-skills/agent-browser`, `~/.ai-pro-skills/SF`, `~/.ai-pro-skills/google-workspace`, `~/.ai-pro-skills/powerpoint`.
- For **agent-browser**, the binary is global (`agent-browser …`); the local folder is only the skill stub.
- For **sf**, Salesforce skill trees live in `~/.ai-skills/sf-skills/skills/{skills_dir}`.
- Re-run `/ai-pro-skills` anytime to **pull + ask targets/skills again + re-copy**.

## Notes

- Never write into `~/.cursor/skills-cursor/` (Cursor built-ins only).
- Prefer `cp` (not move). Keep secrets out of skills.
- Repo: [Acher1234/AI-PRO-SKILLS](https://github.com/Acher1234/AI-PRO-SKILLS.git)
- agent-browser CLI: [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) via npm (this repo only keeps the stub)
- Vendored skills: [google-workspace](https://github.com/NousResearch/hermes-agent/tree/main/skills/productivity/google-workspace), [powerpoint](https://github.com/NousResearch/hermes-agent/tree/main/skills/productivity/powerpoint) (see each `ORIGIN.md`)
