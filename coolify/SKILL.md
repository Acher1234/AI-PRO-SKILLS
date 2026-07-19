---
name: coolify
description: >-
  Query, deploy, and restart applications on Coolify instances. Use when the
  user mentions Coolify, deploy/restart an app, list projects/apps, or invokes
  /coolify_*.
disable-model-invocation: true
---

# coolify

## When to use

Use for Coolify API operations. Trigger phrases: "coolify status", "deploy app", "restart coolify", `/coolify_deploy`, `/coolify_status`.

## Working directory

`~/.ai-pro-skills/coolify`

## Shared environment (see AI-Skills README)

- **Python**: run through the shared venv — `~/.ai-pro-skills/.venv/bin/python coolify.py …` (stdlib-only; if deps are ever added, install once with `~/.ai-pro-skills/install.sh pip init .`). Do not create a per-skill venv.
- **Config**: this skill keeps its **own** `config.json` — placed **next to the installed `SKILL.md`** (the chosen client's skill folder: `~/.cursor/skills/…`, `./.cursor/skills/…` for a project, `$HERMES_HOME/.../…`, etc.), exactly where a `.env` would go. Override with `COOLIFY_CONFIG_PATH` if needed. Never commit the Bearer token.

## Slash commands

| Slash | CLI | Description |
|-------|-----|-------------|
| `/coolify_instances` | `./coolify.py instances` | List configured instances |
| `/coolify_projects` | `./coolify.py projects [instance]` | List projects |
| `/coolify_apps` | `./coolify.py apps <project> [instance]` | List apps in a project |
| `/coolify_discover` | `./coolify.py discover <project> [instance]` | Discover apps (UUIDs) |
| `/coolify_status` | `./coolify.py status <app> [instance]` | App status + last deploy |
| `/coolify_deployments` | `./coolify.py deployments <app> [instance] [-n N]` | Recent deployments |
| `/coolify_deploy` | `./coolify.py deploy <app> [instance] [-f]` | Trigger deploy (`-f` force) |
| `/coolify_restart` | `./coolify.py restart <app> [instance]` | Restart application |

`[instance]` is optional when only one instance is configured. `<app>` is the key from `config.json` → `applications`.

## How to run

1. `cd ~/.ai-pro-skills/coolify`.
2. Ensure `config.json` **next to the installed `SKILL.md`** with instances + app UUID map — see `config.example.json`; `COOLIFY_CONFIG_PATH` overrides.
3. Run the CLI with the shared interpreter: `~/.ai-pro-skills/.venv/bin/python coolify.py <cmd>`; return output.

## Notes

- Python stdlib only; Bearer token in config — never commit secrets.
- Prefer `/coolify_status` before `/coolify_deploy` / `/coolify_restart` when the user is unsure of app health.
