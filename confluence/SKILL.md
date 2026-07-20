---
name: confluence
description: >-
  Confluence via confluence-cli (read, search, create, update, move, delete,
  attachments, comments). Shared npm CLI; per-workspace .env. Use when the user
  mentions Confluence, wiki pages, CQL search, or invokes /confluence_*.
disable-model-invocation: true
---

# confluence

## When to use

Use for Atlassian Confluence page/space work. Triggers: "Confluence page", "wiki",
"search Confluence", "create page", `/confluence_*`.

Confirm with the user before **write** ops (create, update, move, delete, upload).
Prefer `CONFLUENCE_READ_ONLY=true` for research-only agents.

## Working directory (shared library)

`~/.ai-pro-skills/confluence`

Register = copy **only** `SKILL.md`. Do **not** copy the full tree.

## Install CLI (once per machine)

```bash
npm install -g confluence-cli
confluence --version
```

## Credentials (NOT shared — per workspace)

| Scope | `.env` path |
|-------|-------------|
| **Cursor — this project** | `./.cursor/skills/confluence/.env` |
| **Cursor — global** | `~/.cursor/skills/confluence/.env` |
| **Workspace root** | `./.env` (must contain `CONFLUENCE_*`) |
| **Hermes — this profile** | `${HERMES_HOME}/skills/confluence/.env` |
| **Override** | `CONFLUENCE_ENV_PATH=/path/to/.env` |

```bash
mkdir -p ./.cursor/skills/confluence
cp ~/.ai-pro-skills/confluence/SKILL.md ./.cursor/skills/confluence/SKILL.md
cp ~/.ai-pro-skills/confluence/.env.example ./.cursor/skills/confluence/.env
# edit ./.cursor/skills/confluence/.env
```

Required when using direct env config:

| Variable | Example |
|----------|---------|
| `CONFLUENCE_DOMAIN` | `company.atlassian.net` |
| `CONFLUENCE_API_PATH` | `/wiki/rest/api` (Cloud) or `/rest/api` (Server/DC) |
| `CONFLUENCE_AUTH_TYPE` | `basic` or `bearer` |
| `CONFLUENCE_EMAIL` | `user@company.com` (basic only) |
| `CONFLUENCE_API_TOKEN` | API token / PAT |

Optional: `CONFLUENCE_PROFILE`, `CONFLUENCE_READ_ONLY=true`, `CONFLUENCE_FORCE_CLOUD`,
`CONFLUENCE_LINK_STYLE`.

## How to run (agent)

Python is **only** for resolving / checking the `.env`. All Confluence work uses
**`confluence-cli` directly**.

```bash
cd ~/.ai-pro-skills/confluence

# 1) Check .env + binary
python cli.py env-check

# 2) Load credentials into the shell (pick one)
set -a && source "$(python cli.py env-path)" && set +a
# or:  eval "$(python cli.py print-exports)"

# 3) Run confluence-cli
confluence read 123456789 --format markdown
confluence search "deployment pipeline" --limit 20
```

If `CONFLUENCE_DOMAIN` + `CONFLUENCE_API_TOKEN` are already in the process env,
skip sourcing — call `confluence …` directly.

## Slash commands

Map `/confluence_<action>` → `confluence <action> …` (after env is loaded).
Use `python cli.py env-check` / `env-path` / `print-exports` only for setup.

### Setup (Python)

| Slash | CLI | Description |
|-------|-----|-------------|
| `/confluence_env-check` | `python cli.py env-check` | Resolve `.env` + CLI on PATH |
| `/confluence_env-path` | `python cli.py env-path` | Print `.env` path |
| `/confluence_print-exports` | `python cli.py print-exports` | `export` lines for `eval` |

### Read / search (`confluence`)

| Slash | CLI | Description |
|-------|-----|-------------|
| `/confluence_read` | `confluence read <pageId\|URL> [--format markdown\|text\|storage\|html]` | Read page |
| `/confluence_info` | `confluence info <pageId> [--format json]` | Metadata |
| `/confluence_find` | `confluence find "Title" [--space KEY]` | Find by title |
| `/confluence_search` | `confluence search "query" [--limit N] [--cql]` | Search / CQL |
| `/confluence_spaces` | `confluence spaces` | List spaces |
| `/confluence_children` | `confluence children <pageId> [--recursive] [--format json\|tree]` | Children |
| `/confluence_comments` | `confluence comments <pageId> [--format json] [--all]` | List comments |
| `/confluence_attachments` | `confluence attachments <pageId> [--download] [--dest DIR]` | List / download |
| `/confluence_export` | `confluence export <pageId> [--format markdown] [--dest DIR]` | Export |

### Write (`confluence` — confirm first; `--yes` on deletes)

| Slash | CLI | Description |
|-------|-----|-------------|
| `/confluence_create` | `confluence create "Title" SPACE [--file path\|--content …] [--format markdown]` | Create page |
| `/confluence_create-child` | `confluence create-child "Title" <parentId> [--file …] [--format markdown]` | Child page |
| `/confluence_update` | `confluence update <pageId> [--title …] [--file …] [--format markdown]` | Update |
| `/confluence_move` | `confluence move <pageId> <newParentId> [--title …]` | Move (same space) |
| `/confluence_delete` | `confluence delete <pageId> --yes` | Trash page |
| `/confluence_edit` | `confluence edit <pageId> [--output page.xml]` | Fetch storage XML |
| `/confluence_comment` | `confluence comment <pageId> --content "…" [--location footer]` | Add comment |
| `/confluence_comment-delete` | `confluence comment-delete <id> --yes` | Delete comment |
| `/confluence_attachment-upload` | `confluence attachment-upload <pageId> --file path [--replace]` | Upload |
| `/confluence_attachment-delete` | `confluence attachment-delete <pageId> <attId> --yes` | Delete attachment |
| `/confluence_copy-tree` | `confluence copy-tree <src> <parent> [title] [--dry-run]` | Copy page tree |

### Profiles / misc

| Slash | CLI | Description |
|-------|-----|-------------|
| `/confluence_profile_list` | `confluence profile list` | List profiles |
| `/confluence_profile_use` | `confluence profile use <name>` | Switch profile |
| `/confluence_convert` | `confluence convert -i in.md -o out.xml --input-format markdown --output-format storage` | Offline convert |
| `/confluence_api` | `confluence api <endpoint> …` | Raw REST helper |

Global: `confluence --profile staging <command>`.

## Page IDs

Accept numeric IDs or Confluence URLs (`?pageId=`, `/pages/<id>/…`). Prefer ID or
`/pages/<id>` over `/display/<space>/<title>`.

## Agent tips

- Destructive commands: always pass `--yes`.
- Prefer `--format markdown` for agent text; `--format json` for parsing.
- Read-only agents: `CONFLUENCE_READ_ONLY=true` in the workspace `.env`.
- Folders have no body — use `info`, not `read`/`edit`.
- Full reference: `confluence --help` / [confluence-cli](https://www.npmjs.com/package/confluence-cli).

## Files

```
~/.ai-pro-skills/confluence/
├── SKILL.md
├── cli.py              # env-check / env-path / print-exports only
├── _skill_home.py
├── .env.example
└── .gitignore
```

Path helper: [`common/skill_home.py`](../common/skill_home.py).
