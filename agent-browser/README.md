# agent-browser

> Stub skill for [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) — browser automation CLI for AI agents.

This folder only ships the Cursor/Hermes discovery stub (`SKILL.md`). The real CLI and skill content come from npm, not from a vendored source tree.

## Install (once)

```bash
npm i -g agent-browser && agent-browser install
```

`agent-browser install` downloads Chrome for Testing (first time only).

## Use with an agent

1. Install this skill’s `SKILL.md` into Cursor (`~/.cursor/skills/agent-browser/`) or Hermes (`~/.hermes/skills/agent-browser/` or `$HERMES_HOME/skills/agent-browser/`).
2. Before any automation, the agent must load the version-matched guide from the CLI:

```bash
agent-browser skills get core
agent-browser skills get core --full
```

Specialized guides:

```bash
agent-browser skills list
agent-browser skills get electron
agent-browser skills get slack
agent-browser skills get dogfood
agent-browser skills get vercel-sandbox
agent-browser skills get agentcore
```

## Why no full repo here

Upstream `SKILL.md` is intentionally a thin stub. Workflows, command references, and templates are served by `agent-browser skills get …` so they always match the installed npm version. Cloning the whole [agent-browser](https://github.com/vercel-labs/agent-browser) repo is only needed if you develop or patch the tool itself.

## Files

| File | Role |
|------|------|
| `SKILL.md` | Discovery stub for Cursor / Hermes |
| `README.md` | This file |

## Upstream

- GitHub: [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)
- npm: `agent-browser`
