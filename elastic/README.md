# Elastic — Elastic Agent Skills installer

Meta-skill that syncs [elastic/agent-skills](https://github.com/elastic/agent-skills.git) into `~/.ai-skills/elastic-agent-skills` and copies selected skills into Cursor or Hermes.

## Install this meta-skill

Copy `elastic/SKILL.md` to:

- Cursor: `~/.cursor/skills/elastic/SKILL.md`
- Hermes: `~/.hermes/skills/elastic/SKILL.md` or `$HERMES_HOME/skills/elastic/SKILL.md`

Then invoke `/elastic` (or `/elastic_update`) in the agent.

## What `/elastic` does

1. `git clone` / `git pull` → `~/.ai-skills/elastic-agent-skills`
2. Asks Cursor vs Hermes (and Hermes profile scope)
3. Lists skills **by category** (Cloud, Elasticsearch, Kibana, Observability, Security) — not a flat dump of every folder
4. Copies chosen skill folders (or `SKILL.md`) into the destination, and **prepends a shared-env / working-dir header** to each installed `SKILL.md`
5. On every recall: **re-proposes an update**

Working dir once installed: `~/.ai-skills/elastic-agent-skills/skills/{category}/{skill}`

## Working directory

Elastic skills are nested two levels (category → skill). For any installed Elastic skill:

```text
~/.ai-skills/elastic-agent-skills/skills/{category}/{skill}
```

Agents should run scripts and open `references/` / `assets/` from that path (the shared environment), not the Cursor/Hermes stub.

## Dest name rule

`dest = leaf` if the leaf folder already starts with `<category>-`, otherwise `dest = <category>-<leaf>` — reproduces upstream names:

| Upstream | Installed as |
|----------|--------------|
| `skills/cloud/access-management` | `cloud-access-management` |
| `skills/elasticsearch/elasticsearch-esql` | `elasticsearch-esql` |
| `skills/kibana/agent-builder` | `kibana-agent-builder` |
| `skills/kibana/kibana-alerting-rules` | `kibana-alerting-rules` |
| `skills/observability/logs-search` | `observability-logs-search` |
| `skills/security/alert-triage` | `security-alert-triage` |

## Credentials — shared `.env`

Every skill installed via `/elastic` shares one Elastic `.env`, resolved through `common/skill_home.py` (`SkillHome("elastic")`):

```dotenv
ELASTICSEARCH_URL=https://your-cluster.es.example.com:9200
ELASTICSEARCH_USERNAME=your_username
ELASTICSEARCH_PASSWORD=your_password
```

Before using any skill: copy `.env.example` → `.env` in the destination (e.g. `~/.cursor/skills/elastic/.env`) and fill it in. Each installed `SKILL.md` gets a prepended header telling the agent to source it:

```bash
ELASTIC_ENV="$(python3 ~/.ai-pro-skills/elastic/_skill_home.py)"
set -a; . "$ELASTIC_ENV"; set +a
```

Override the path with `ELASTIC_ENV_PATH`. Never commit the real `.env`.

## Files

| File | Role |
|------|------|
| `SKILL.md` | Install / update prompt for agents |
| `_skill_home.py` | Resolves the shared `.env` via `common/skill_home.py` (prints the path when run) |
| `.env.example` | Template for the shared Elastic credentials |
| `README.md` | This file |

## Upstream

- [elastic/agent-skills](https://github.com/elastic/agent-skills.git)
- Optional: `npx skills add elastic/agent-skills`
