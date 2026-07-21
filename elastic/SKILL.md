---
name: elastic
description: >-
  Meta-skill installer for the official Elastic Agent Skills
  (github.com/elastic/agent-skills). Syncs the upstream repo and installs
  selected Elasticsearch / Kibana / Observability / Security / Cloud skills into
  the user's Cursor or Hermes skills directory, using a shared working
  directory. Use when the user asks for Elastic / Elasticsearch / Kibana / ES|QL
  / Observability / Elastic Security skills, says "install elastic skills" /
  "update elastic skills", or invokes `/elastic`.
disable-model-invocation: true
---

# Elastic — Elastic Agent Skills installer (Cursor or Hermes)

Meta-skill that syncs [elastic/agent-skills](https://github.com/elastic/agent-skills.git) and installs selected Elastic agent skills into the user's Cursor or Hermes skills directory.

Upstream skills evolve quickly (renames, restructures, new releases). Prefer this repo as the source of truth and re-run `/elastic` often to update.

## When to use

- User asks for Elastic / Elasticsearch / Kibana / ES|QL / Observability / Elastic Security / Elastic Cloud skills
- User says "install elastic skills", "update elastic skills", or invokes `/elastic`
- **Every time this skill is recalled:** re-propose an update (pull + re-list by category + re-copy) — do not assume the local copy is current

## Working directory

Elastic skills are nested **two levels** (category → skill) upstream. Installed skill trees live under:

```text
~/.ai-skills/elastic-agent-skills/skills/{category}/{skill}
```

Example: `~/.ai-skills/elastic-agent-skills/skills/elasticsearch/elasticsearch-esql`

When running scripts or reading `references/` / `assets/` / `scripts/` for an installed Elastic skill, **always `cd` into that working directory** (`~/.ai-skills/elastic-agent-skills/skills/{category}/{skill}`), not the Cursor/Hermes stub path.

## Credentials — shared Elastic `.env`

Every skill installed via `/elastic` shares **one** Elastic `.env`, resolved through
`common/skill_home.py` (`SkillHome("elastic").env_path()`), so each Cursor project /
Hermes profile can point at a different cluster.

Required variables:

```dotenv
ELASTICSEARCH_URL=https://your-cluster.es.example.com:9200
ELASTICSEARCH_USERNAME=your_username
ELASTICSEARCH_PASSWORD=your_password
```

**Before running any installed Elastic skill you MUST first create the `.env`:**

1. A `.env.example` template ships next to this meta-skill (`elastic/.env.example`).
   If the destination has no `.env.example`, **copy it there first** so users know
   what to fill in.
2. Copy `.env.example` → `.env` in the chosen destination and fill in the three
   `ELASTICSEARCH_*` values (never commit the real `.env`).

Resolve / source the `.env` from a shell (uses `common/skill_home.py`):

```bash
# Prints the resolved per-workspace .env path, then source it.
ELASTIC_ENV="$(python3 ~/.ai-pro-skills/elastic/_skill_home.py)"
set -a; . "$ELASTIC_ENV"; set +a   # exports ELASTICSEARCH_URL / _USERNAME / _PASSWORD
```

| Scope | `.env` path |
|-------|-------------|
| **Cursor — this project** | `./.cursor/skills/elastic/.env` |
| **Cursor — global** | `~/.cursor/skills/elastic/.env` |
| **Hermes — this profile** | `${HERMES_HOME}/skills/elastic/.env` |
| **Override** | `ELASTIC_ENV_PATH=/path/to/.env` |

## Critical — ask the user first

**Do not copy every Elastic skill blindly.** Upstream explicitly warns against installing everything: each installed skill adds routing context evaluated on every request. After sync, ask in this order:

### 1) Target platform

> Install Elastic skills for **Cursor**, **Hermes**, or **both**?

| Target | Skills directory |
|--------|------------------|
| **Cursor** | `~/.cursor/skills/<skill-name>/SKILL.md` |
| **Hermes — all profiles** | `~/.hermes/skills/<skill-name>/SKILL.md` |
| **Hermes — this profile only** | `${HERMES_HOME}/skills/<skill-name>/SKILL.md` |

### 2) If Hermes (or both): profile scope

> For Hermes, install for **all profiles** (`~/.hermes/skills/`) or **this profile only** (`$HERMES_HOME/skills/`)?

- If **this profile**: require `HERMES_HOME`; if unset, ask for the profile path.
- If **all**: use `~/.hermes/skills/` (create if missing).

### 3) Which Elastic skills — **by category** (do not dump the full list)

Build a **numbered index** from `~/.ai-skills/elastic-agent-skills/skills/*/*/SKILL.md` (two levels, alphabetical), then show the user a **category table** with a few example names. Rebuild ranges from the current index — numbers drift when upstream adds/renames skills.

> **3) Quels skills ?**  
> Réponds `all`, des numéros, des plages, des catégories, ou des noms. Exemples utiles :

| Catégorie | Exemples de skills |
|-----------|--------------------|
| **Cloud** (5) | `cloud-setup`, `cloud-access-management`, `cloud-create-project`, `cloud-manage-project`, `cloud-network-security` |
| **Elasticsearch** (7) | `elasticsearch-esql`, `elasticsearch-authn`, `elasticsearch-authz`, `elasticsearch-audit`, `elasticsearch-file-ingest`, `elasticsearch-onboarding`, `elasticsearch-security-troubleshooting` |
| **Kibana** (8) | `kibana-dashboards`, `kibana-alerting-rules`, `kibana-connectors`, `kibana-agent-builder`, `kibana-anomaly-detection`, `kibana-audit`, `kibana-vega`, `kibana-streams` |
| **Observability** (11) | `observability-logs-search`, `observability-service-health`, `observability-manage-slos`, `observability-k8s-investigation`, `observability-llm-obs`, `observability-edot-*-instrument/migrate` |
| **Security** (4) | `security-alert-triage`, `security-case-management`, `security-detection-rule-management`, `security-generate-security-sample-data` |

> **Tip (from Elastic):** don't install every skill. Start with **`cloud-setup`** + the **elasticsearch auth** skills (`elasticsearch-authn`, `elasticsearch-authz`) — most other skills depend on credentials — then add only the skills relevant to the workflow.

Working dir once installed: `~/.ai-skills/elastic-agent-skills/skills/{category}/{skill}`

Examples of answers: `Cursor + all` · `Elasticsearch + Kibana` · `elasticsearch-esql, kibana-dashboards, cloud-setup` · `Observability` · numbers / ranges from the index.

**Category → upstream folder** (use these to bucket the alphabetical index):

| Catégorie | Upstream folder | Dest name rule |
|-----------|-----------------|----------------|
| Cloud | `skills/cloud/*` | `cloud-<leaf>` |
| Elasticsearch | `skills/elasticsearch/*` | `<leaf>` (already `elasticsearch-*`) |
| Kibana | `skills/kibana/*` | `<leaf>` if it starts with `kibana-`, else `kibana-<leaf>` |
| Observability | `skills/observability/*` | `observability-<leaf>` |
| Security | `skills/security/*` | `security-<leaf>` |

> **Dest name rule (general):** `dest = leaf` if the leaf folder already starts with `<category>-`, otherwise `dest = <category>-<leaf>`. This reproduces the upstream skill names (e.g. `cloud/access-management` → `cloud-access-management`, `kibana/agent-builder` → `kibana-agent-builder`, `elasticsearch/elasticsearch-esql` → `elasticsearch-esql`).

Only if the user asks for the **full** catalog should you print every folder name.

Always also keep this meta skill `elastic` available in the chosen destination(s) when installing from AI-PRO-SKILLS.

## Prompt (do this)

```
Source: https://github.com/elastic/agent-skills.git
Local cache: ~/.ai-skills/elastic-agent-skills

If ~/.ai-skills/elastic-agent-skills already exists:
  - cd ~/.ai-skills/elastic-agent-skills
  - git pull --ff-only   (or fetch + reset --hard origin/main if pull conflicts and user agrees)
Else:
  - mkdir -p ~/.ai-skills
  - git clone --depth 1 https://github.com/elastic/agent-skills.git ~/.ai-skills/elastic-agent-skills

IMPORTANT — every time /elastic is invoked:
1. Sync (pull/clone) first.
2. Ask Cursor vs Hermes vs both.
3. If Hermes: ask all profiles vs this profile ($HERMES_HOME).
4. Index skills under ~/.ai-skills/elastic-agent-skills/skills/*/*/SKILL.md (TWO levels)
   alphabetically.
5. Show a CATEGORY table (Cloud, Elasticsearch, Kibana, Observability, Security)
   with a few example names — do NOT dump every skill unless the user asks.
   Remind the user of Elastic's tip: don't install everything; start with
   cloud-setup + elasticsearch auth.
6. Ask which to install/update (all / categories / numbers / names).
Do not copy all by default unless the user says "all".

7. CREDENTIALS — before installing/using any skill, make sure a `.env.example`
   exists in the destination and a `.env` is created from it:
   - Copy this meta-skill's `.env.example` (elastic/.env.example) into $DEST/elastic/
     if it is not already there.
   - Copy `.env.example` -> `.env` in $DEST/elastic/ and fill in:
       ELASTICSEARCH_URL / ELASTICSEARCH_USERNAME / ELASTICSEARCH_PASSWORD
   - The `.env` is resolved by common/skill_home.py (SkillHome("elastic")).

Then for EACH selected skill:
  Upstream tree:  ~/.ai-skills/elastic-agent-skills/skills/{category}/{leaf}/
  Dest name:      dest = leaf if leaf starts with "{category}-", else "{category}-{leaf}"
  Copy the skill folder to:
    Cursor:         ~/.cursor/skills/{dest}/
    Hermes all:     ~/.hermes/skills/{dest}/
    Hermes profile: $HERMES_HOME/skills/{dest}/

  Prefer copying the FULL skill folder (SKILL.md + scripts/ + references/ + assets/)
  into the destination so agents can run bundled scripts. If the destination
  already exists, refresh it (rsync/cp -R) so updates replace stale files.

  PREPEND a shared-env header at the TOP of each installed SKILL.md (after its
  front-matter) that states:
    (a) the working directory to run scripts / read references/ + assets/ from:
          ~/.ai-skills/elastic-agent-skills/skills/{category}/{leaf}
    (b) that BEFORE running anything the agent must SOURCE the shared Elastic .env,
        resolved via common/skill_home.py, e.g.:
          ELASTIC_ENV="$(python3 ~/.ai-pro-skills/elastic/_skill_home.py)"
          set -a; . "$ELASTIC_ENV"; set +a
        (exports ELASTICSEARCH_URL / ELASTICSEARCH_USERNAME / ELASTICSEARCH_PASSWORD)
  (Python skills use the shared venv ~/.ai-skills/.venv/bin/python.)

Reload Cursor if Cursor was a target. For Hermes, reload/restart the agent if needed.
```

## Agent checklist

1. Clone or pull `~/.ai-skills/elastic-agent-skills` from [elastic/agent-skills](https://github.com/elastic/agent-skills.git).
2. **Re-propose update** every time this skill is used (tell the user local Elastic skills can be refreshed).
3. Ask **Cursor / Hermes / both**.
4. If Hermes: ask **all** vs **this profile**; resolve `HERMES_HOME` if needed.
5. Build alphabetical index of `skills/*/*/SKILL.md` → present **by category** (examples); ask which to install/update. Remind of the "don't install everything" tip.
6. **Credentials:** ensure `.env.example` exists in `$DEST/elastic/` (copy this meta-skill's `.env.example` if missing), then create `.env` from it with `ELASTICSEARCH_URL` / `ELASTICSEARCH_USERNAME` / `ELASTICSEARCH_PASSWORD` (resolved via `common/skill_home.py`).
7. Copy selected skill folders (or at least each `SKILL.md`) into every chosen destination, and **prepend a shared-env header** to the top of each installed `SKILL.md` — it must (a) give the working dir `~/.ai-skills/elastic-agent-skills/skills/{category}/{leaf}` and (b) tell the agent to **source the shared Elastic `.env`** via `common/skill_home.py` before running anything. See the snippet in "Copy map".
8. Remind: working directory for Elastic skill work is `~/.ai-skills/elastic-agent-skills/skills/{category}/{leaf}`.
9. Tell the user to reload Cursor and/or Hermes.

## Copy map (reference)

| Source | Target |
|--------|--------|
| `~/.ai-skills/elastic-agent-skills/skills/{category}/{leaf}/` | `$DEST/{dest}/` (full tree preferred) |
| `~/.ai-skills/elastic-agent-skills/skills/{category}/{leaf}/SKILL.md` | `$DEST/{dest}/SKILL.md` (minimum) |

`$DEST` ∈ `~/.cursor/skills` · `~/.hermes/skills` · `$HERMES_HOME/skills`

```bash
# Sync library
mkdir -p ~/.ai-skills
if [ -d ~/.ai-skills/elastic-agent-skills/.git ]; then
  git -C ~/.ai-skills/elastic-agent-skills pull --ff-only
else
  git clone --depth 1 https://github.com/elastic/agent-skills.git ~/.ai-skills/elastic-agent-skills
fi

# List skills (for indexing — show CATEGORIES to the user, not this raw dump).
# Two levels deep: skills/{category}/{leaf}/SKILL.md
find ~/.ai-skills/elastic-agent-skills/skills -mindepth 2 -maxdepth 2 -type d | sort

# Example: Cursor + one skill (+ prepend a shared-env / working-dir header to SKILL.md)
CATEGORY=elasticsearch
LEAF=elasticsearch-esql
# dest = leaf if it already starts with "$CATEGORY-", else "$CATEGORY-$LEAF"
case "$LEAF" in
  "$CATEGORY"-*) DEST_NAME="$LEAF" ;;
  *)             DEST_NAME="$CATEGORY-$LEAF" ;;
esac
SRC=~/.ai-skills/elastic-agent-skills/skills/"$CATEGORY"/"$LEAF"
DEST=~/.cursor/skills
mkdir -p "$DEST/$DEST_NAME"
cp -R "$SRC"/. "$DEST/$DEST_NAME"/

# Ensure the shared .env.example lives next to the elastic meta-skill in $DEST
mkdir -p "$DEST/elastic"
[ -f "$DEST/elastic/.env.example" ] || cp ~/.ai-pro-skills/elastic/.env.example "$DEST/elastic/.env.example" 2>/dev/null || true

# Shared-env header: working dir + source the Elastic .env (via common/skill_home.py)
NOTE="> **Installed via /elastic — shared environment.**
>
> **Working dir** (scripts, \`references/\`, \`assets/\`): \`~/.ai-skills/elastic-agent-skills/skills/$CATEGORY/$LEAF\` (not this stub path). Python skills use the shared venv \`~/.ai-skills/.venv/bin/python\`.
>
> **Before running anything, source the shared Elastic \`.env\`** (resolved via \`common/skill_home.py\`):
> \`\`\`bash
> ELASTIC_ENV=\"\$(python3 ~/.ai-pro-skills/elastic/_skill_home.py)\"
> set -a; . \"\$ELASTIC_ENV\"; set +a   # ELASTICSEARCH_URL / ELASTICSEARCH_USERNAME / ELASTICSEARCH_PASSWORD
> \`\`\`"
f="$DEST/$DEST_NAME/SKILL.md"
if [ -f "$f" ]; then
  awk -v note="$NOTE" '
    NR==1 && $0=="---" {print; fm=1; next}
    fm && $0=="---" && !done {print; print ""; print note; done=1; next}
    {print}
  ' "$f" > "$f.tmp"
  grep -qF "$NOTE" "$f.tmp" || { printf "%s\n\n" "$NOTE" | cat - "$f" > "$f.tmp"; }
  mv "$f.tmp" "$f"
fi
```

## Slash commands

| Slash | Action |
|-------|--------|
| `/elastic` | Sync elastic/agent-skills, ask targets, list **by category**, install/update selection |
| `/elastic_update` | Same as `/elastic` — force refresh pull + re-copy |
| `/elastic_list` | Sync (if needed) and show the **category table** (full names only if asked) |

## Notes

- Library cache: `~/.ai-skills/elastic-agent-skills` (full git clone of upstream).
- Per-skill working directory: `~/.ai-skills/elastic-agent-skills/skills/{category}/{leaf}` (two levels deep — unlike sf-skills which is one level).
- Shared credentials: one `.env` per workspace with `ELASTICSEARCH_URL` / `ELASTICSEARCH_USERNAME` / `ELASTICSEARCH_PASSWORD`, resolved via `common/skill_home.py` (`SkillHome("elastic")`); template in `elastic/.env.example`. Override path with `ELASTIC_ENV_PATH`. Never commit the real `.env` or any API key; scope credentials to least privilege and prefer read-only until validated.
- Alternative upstream installs: `npx skills add elastic/agent-skills`, `claude plugin marketplace add https://github.com/elastic/agent-skills`. This meta-skill prefers the explicit `~/.ai-skills` cache + user-chosen Cursor/Hermes destinations with a shared working directory.
- Upstream: [elastic/agent-skills](https://github.com/elastic/agent-skills.git)
