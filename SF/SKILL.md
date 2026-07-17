---
name: sf
description: >-
  Install or update Salesforce agent skills from forcedotcom/sf-skills. Clone/pull
  the library under ~/.ai-skills/sf-skills, present skills by theme (not a flat
  dump), ask Cursor vs Hermes destination, then copy chosen skills. Use when the
  user wants Salesforce / Agentforce / Apex / LWC / Flow / SOQL skills, syncs
  sf-skills, or runs /sf to refresh Salesforce skills.
disable-model-invocation: true
---

# SF — Salesforce skills installer (Cursor or Hermes)

Meta-skill that syncs [forcedotcom/sf-skills](https://github.com/forcedotcom/sf-skills.git) and installs selected Salesforce agent skills into the user’s Cursor or Hermes skills directory.

Upstream skills evolve quickly (renames, restructures). Prefer this repo as the source of truth and re-run `/sf` often to update.

## When to use

- User asks for Salesforce / Agentforce / Apex / LWC / Flow / SOQL / Data Cloud skills
- User says “install Salesforce skills”, “update sf-skills”, or invokes `/sf`
- **Every time this skill is recalled:** re-propose an update (pull + re-list by theme + re-copy) — do not assume the local copy is current

## Working directory

Salesforce skill trees live under:

```text
~/.ai-skills/sf-skills/skills/{skills_dir}
```

Example: `~/.ai-skills/sf-skills/skills/platform-apex-generate`

When running scripts or reading `references/` / `assets/` for an installed SF skill, **always `cd` into that working directory** (`~/.ai-skills/sf-skills/skills/{skills_dir}`), not the Cursor/Hermes stub path.

## Critical — ask the user first

**Do not copy every Salesforce skill blindly.** After sync, ask in this order:

### 1) Target platform

> Install SF skills for **Cursor**, **Hermes**, or **both**?

| Target | Skills directory |
|--------|------------------|
| **Cursor** | `~/.cursor/skills/<skill-name>/SKILL.md` |
| **Hermes — all profiles** | `~/.hermes/skills/<skill-name>/SKILL.md` |
| **Hermes — this profile only** | `${HERMES_HOME}/skills/<skill-name>/SKILL.md` |

### 2) If Hermes (or both): profile scope

> For Hermes, install for **all profiles** (`~/.hermes/skills/`) or **this profile only** (`$HERMES_HOME/skills/`)?

- If **this profile**: require `HERMES_HOME`; if unset, ask for the profile path.
- If **all**: use `~/.hermes/skills/` (create if missing).

### 3) Which Salesforce skills — **by theme** (do not dump the full list)

**Do not list every submodule / skill folder as a flat wall of names.** After sync, build a **numbered index** of `~/.ai-skills/sf-skills/skills/*/SKILL.md` (alphabetical), then show the user a **theme table** with number ranges + a few example names.

Present roughly like this (rebuild ranges from the current index — numbers drift when upstream adds/renames skills):

> **3) Quels skills ?**  
> Réponds `all`, des numéros, des plages, des thèmes, ou des noms. Exemples utiles :

| Groupe | Exemples |
|--------|----------|
| **Agentforce** | `1–5` |
| **Platform / Apex / SOQL** | `62–90` — ex. `platform-apex-generate`, `platform-soql-query` |
| **Flow** | `6` — ex. `automation-flow-generate` |
| **Data 360** | `10–18` |
| **DX / org** | `22–32` |
| **Experience / LWC / UI bundles** | `33–45` |
| **OmniStudio** | `54–61` |
| **Commerce** | `7–9` |
| **Design Systems (SLDS)** | `19–21` |
| **Integration / Connected App / CDC** | `47–50` |
| **Mobile** | `51–53` |
| **External / other** | remaining numbers (ex. diagrams) |

Working dir once installed: `~/.ai-skills/sf-skills/skills/{skills_dir}`

Examples of answers: `Cursor + all` · `64,65,66,67,85` · `platform-apex-generate, platform-soql-query, automation-flow-generate` · `Platform / Apex / SOQL` · `Agentforce + Flow`

**Theme → name prefixes** (use these to bucket the alphabetical list):

| Theme | Prefixes |
|-------|----------|
| Agentforce | `agentforce-` |
| Flow | `automation-flow-` |
| Commerce | `commerce-` |
| Data 360 | `data360-` |
| Design Systems | `design-systems-` |
| DX / org | `dx-` |
| Experience / LWC / UI | `experience-` |
| External | `external-` |
| Integration | `integration-` |
| Mobile | `mobile-` |
| OmniStudio | `omnistudio-` |
| Platform / Apex / SOQL | `platform-` |

Accept: `all`, theme names, number ranges (`64-67`), individual numbers, or skill folder names.

Only if the user asks for the **full** catalog should you print every folder name.

Always also keep this meta skill `sf` available in the chosen destination(s) when installing from AI-PRO-SKILLS.

## Prompt (do this)

```
Source: https://github.com/forcedotcom/sf-skills.git
Local cache: ~/.ai-skills/sf-skills

If ~/.ai-skills/sf-skills already exists:
  - cd ~/.ai-skills/sf-skills
  - git pull --ff-only   (or fetch + reset --hard origin/main if pull conflicts and user agrees)
Else:
  - mkdir -p ~/.ai-skills
  - git clone --depth 1 https://github.com/forcedotcom/sf-skills.git ~/.ai-skills/sf-skills

IMPORTANT — every time /sf is invoked:
1. Sync (pull/clone) first.
2. Ask Cursor vs Hermes vs both.
3. If Hermes: ask all profiles vs this profile ($HERMES_HOME).
4. Index skills under ~/.ai-skills/sf-skills/skills/*/SKILL.md alphabetically.
5. Show a THEME table (Agentforce, Platform/Apex/SOQL, Flow, Data 360, DX/org,
   Experience/LWC/UI, OmniStudio, + other clusters) with number ranges + a few
   example names — do NOT dump every skill unless the user asks.
6. Ask which to install/update (all / themes / numbers / names).
Do not copy all by default unless the user says "all".

Then for EACH selected skill (folder name = skills_dir):
  Source tree:  ~/.ai-skills/sf-skills/skills/{skills_dir}/
  Copy SKILL.md to:
    Cursor:  ~/.cursor/skills/{skills_dir}/SKILL.md
    Hermes all:     ~/.hermes/skills/{skills_dir}/SKILL.md
    Hermes profile: $HERMES_HOME/skills/{skills_dir}/SKILL.md

  Prefer copying the FULL skill folder (SKILL.md + scripts/ + references/ + assets/)
  into the destination so agents can run bundled scripts. If the destination
  already exists, refresh it (rsync/cp -R) so updates replace stale files.

  Ensure the installed SKILL.md documents (or the agent remembers) the working
  directory:
    ~/.ai-skills/sf-skills/skills/{skills_dir}

Reload Cursor if Cursor was a target. For Hermes, reload/restart the agent if needed.
```

## Agent checklist

1. Clone or pull `~/.ai-skills/sf-skills` from [forcedotcom/sf-skills](https://github.com/forcedotcom/sf-skills.git).
2. **Re-propose update** every time this skill is used (tell the user local SF skills can be refreshed).
3. Ask **Cursor / Hermes / both**.
4. If Hermes: ask **all** vs **this profile**; resolve `HERMES_HOME` if needed.
5. Build alphabetical index → present **by theme** (ranges + examples); ask which to install/update.
6. Copy selected skill folders (or at least each `SKILL.md`) into every chosen destination.
7. Remind: working directory for SF skill work is `~/.ai-skills/sf-skills/skills/{skills_dir}`.
8. Tell the user to reload Cursor and/or Hermes.

## Copy map (reference)

| Source | Target |
|--------|--------|
| `~/.ai-skills/sf-skills/skills/{skills_dir}/` | `$DEST/{skills_dir}/` (full tree preferred) |
| `~/.ai-skills/sf-skills/skills/{skills_dir}/SKILL.md` | `$DEST/{skills_dir}/SKILL.md` (minimum) |

`$DEST` ∈ `~/.cursor/skills` · `~/.hermes/skills` · `$HERMES_HOME/skills`

```bash
# Sync library
mkdir -p ~/.ai-skills
if [ -d ~/.ai-skills/sf-skills/.git ]; then
  git -C ~/.ai-skills/sf-skills pull --ff-only
else
  git clone --depth 1 https://github.com/forcedotcom/sf-skills.git ~/.ai-skills/sf-skills
fi

# List skill dirs (for indexing — show themes to the user, not this raw dump)
ls -1 ~/.ai-skills/sf-skills/skills

# Example: Cursor + one skill
SKILL_DIR=platform-apex-generate
DEST=~/.cursor/skills
mkdir -p "$DEST/$SKILL_DIR"
cp -R ~/.ai-skills/sf-skills/skills/"$SKILL_DIR"/. "$DEST/$SKILL_DIR"/
```

## Slash commands

| Slash | Action |
|-------|--------|
| `/sf` | Sync sf-skills, ask targets, list **by theme**, install/update selection |
| `/sf_update` | Same as `/sf` — force refresh pull + re-copy |
| `/sf_list` | Sync (if needed) and show the **theme table** (full names only if asked) |

## Notes

- Library cache: `~/.ai-skills/sf-skills` (full git clone of upstream).
- Per-skill working directory: `~/.ai-skills/sf-skills/skills/{skills_dir}`.
- Do not commit org credentials or `.forceignore` secrets into skills.
- Alternative upstream install: `npx skills add forcedotcom/sf-skills` — this meta-skill prefers the explicit `~/.ai-skills` cache + user-chosen Cursor/Hermes destinations.
- Upstream: [forcedotcom/sf-skills](https://github.com/forcedotcom/sf-skills.git)
