# SF — Salesforce skills installer

Meta-skill that syncs [forcedotcom/sf-skills](https://github.com/forcedotcom/sf-skills.git) into `~/.ai-skills/sf-skills` and copies selected skills into Cursor or Hermes.

## Install this meta-skill

Copy `SF/SKILL.md` to:

- Cursor: `~/.cursor/skills/sf/SKILL.md`
- Hermes: `~/.hermes/skills/sf/SKILL.md` or `$HERMES_HOME/skills/sf/SKILL.md`

Then invoke `/sf` (or `/sf_update`) in the agent.

## What `/sf` does

1. `git clone` / `git pull` → `~/.ai-skills/sf-skills`
2. Asks Cursor vs Hermes (and Hermes profile scope)
3. Lists skills **by theme** (Agentforce, Platform/Apex/SOQL, Flow, Data 360, DX/org, Experience/LWC/UI, OmniStudio, …) — not a flat dump of every folder
4. Copies chosen skill folders (or `SKILL.md`) into the destination
5. On every recall: **re-proposes an update**

Working dir once installed: `~/.ai-skills/sf-skills/skills/{skills_dir}`

## Working directory

For any installed Salesforce skill:

```text
~/.ai-skills/sf-skills/skills/{skills_dir}
```

Agents should run scripts and open references from that path.

## Files

| File | Role |
|------|------|
| `SKILL.md` | Install / update prompt for agents |
| `README.md` | This file |

## Upstream

- [forcedotcom/sf-skills](https://github.com/forcedotcom/sf-skills.git)
- Optional: `npx skills add forcedotcom/sf-skills`
