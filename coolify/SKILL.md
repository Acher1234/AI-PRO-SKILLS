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
2. Ensure `config.json` (or `COOLIFY_CONFIG_PATH`) with instances + app UUID map — see `config.example.json`.
3. Run the CLI for the slash command; return output.

## Notes

- Python stdlib only; Bearer token in config — never commit secrets.
- Prefer `/coolify_status` before `/coolify_deploy` / `/coolify_restart` when the user is unsure of app health.
