# 🧰 AI-PRO-SKILLS

> Professional / ops CLI skills for Cursor & Hermes (Coolify, Zscaler, agent-browser, Google Workspace, PowerPoint, …).  
> Standalone repository — not a nested copy of [AI-Skills](https://github.com/Acher1234/AI-Skills).

Repo: [github.com/Acher1234/AI-PRO-SKILLS](https://github.com/Acher1234/AI-PRO-SKILLS.git)

## 📁 Structure

```
AI-PRO-SKILLS/
├── README.md               ← This file
├── SKILL.md                ← Cursor install prompt (default → ~/.ai-pro-skills)
├── SKILL_TEMPLATE.md       ← How to add a new skill
├── coolify/                ← Coolify deploy / status / restart CLI
├── zscaler/                ← Zscaler ZPA / ZIA / ZIdentity CLI
├── agent-browser/          ← Stub skill (CLI via npm)
├── SF/                     ← Install/update Salesforce skills (forcedotcom/sf-skills)
├── google-workspace/       ← Vendored: Gmail / Calendar / Drive / Docs / Sheets
└── powerpoint/             ← Vendored: create / edit PowerPoint decks
```

> **Install :** colle le [prompt](#-install-prompt-cursor-or-hermes) ou suis [`SKILL.md`](SKILL.md). Cibles : Cursor (`~/.cursor/skills`), Hermes all (`~/.hermes/skills`), ou Hermes profile (`$HERMES_HOME/skills`).

## 📋 Skills

| Skill | Description | Language / notes |
|-------|-------------|------------------|
| `coolify` | Coolify instances — status, deploy, restart | python |
| `zscaler` | Zscaler admin — ZPA / ZIA / ZIdentity | python |
| `agent-browser` | Browser automation CLI for AI agents (navigate, click, fill, screenshot, scrape) | stub + `npm i -g agent-browser` ([upstream](https://github.com/vercel-labs/agent-browser)) |
| `sf` | Install / update Salesforce skills from [forcedotcom/sf-skills](https://github.com/forcedotcom/sf-skills.git) | sync → `~/.ai-skills/sf-skills`, copy to Cursor/Hermes |
| `google-workspace` | Gmail, Calendar, Drive, Docs, Sheets (OAuth + CLI) | vendored from [hermes-agent](https://github.com/NousResearch/hermes-agent/tree/main/skills/productivity/google-workspace) |
| `powerpoint` | Create / edit PowerPoint presentations | vendored from [hermes-agent](https://github.com/NousResearch/hermes-agent/tree/main/skills/productivity/powerpoint) |

## 🪄 Install prompt (Cursor or Hermes)

Paste into an **Agent** chat. Root [`SKILL.md`](SKILL.md) (`/ai-pro-skills`) is the same flow.

> The AI must ask: **1)** Cursor / Hermes / both → **2)** if Hermes: all profiles vs this profile → **3)** which skills (including `agent-browser`, `sf`, `google-workspace`, `powerpoint`).

| Target | Install directory |
|--------|-------------------|
| Cursor | `~/.cursor/skills/<skill>/SKILL.md` |
| Hermes — all profiles | `~/.hermes/skills/<skill>/SKILL.md` |
| Hermes — this profile | `${HERMES_HOME}/skills/<skill>/SKILL.md` |

```
Take the project at url: https://github.com/Acher1234/AI-PRO-SKILLS.git
Install under ~ as .ai-pro-skills (pull if it exists).

Ask: Cursor vs Hermes vs both.
If Hermes: all profiles (~/.hermes/skills) vs this profile ($HERMES_HOME/skills).
List skills (coolify, zscaler, agent-browser, sf, google-workspace, powerpoint) and ask which to install.
Copy only chosen skills (+ always ai-pro-skills) into each selected destination.
For google-workspace / powerpoint: copy the whole folder (not only SKILL.md).
  Cursor → $DEST/<skill>/
  Hermes → $DEST/productivity/<skill>/  (matches upstream paths)
```

| Step | Action |
|------|--------|
| 1 | Clone / pull `~/.ai-pro-skills` |
| 2 | Ask **Cursor / Hermes / both** |
| 3 | If Hermes: **all** or **this profile** |
| 4 | List skills and ask which |
| 5 | Copy into chosen destination(s) |
| 6 | Reload Cursor and/or Hermes |

## 📂 Working directories

| Skill | Working directory |
|-------|-------------------|
| `coolify` | `~/.ai-pro-skills/coolify` |
| `zscaler` | `~/.ai-pro-skills/zscaler` |
| `agent-browser` | global CLI after npm install (`agent-browser …`); stub in `~/.ai-pro-skills/agent-browser` |
| `sf` | meta-skill in `~/.ai-pro-skills/SF`; SF skills cache: `~/.ai-skills/sf-skills/skills/{skills_dir}` |
| `google-workspace` | `~/.ai-pro-skills/google-workspace` (scripts under `scripts/`) |
| `powerpoint` | `~/.ai-pro-skills/powerpoint` (scripts + editing guides) |

The agent must `cd` into the skill dir when running local CLIs; for `agent-browser`, prefer the global binary after `npm i -g agent-browser && agent-browser install`.

## 🧩 Create a new skill

See **[`SKILL_TEMPLATE.md`](SKILL_TEMPLATE.md)** (structure, `SKILL.md`, slash `/{skill}_{command}`, security).

## 🎯 Register skills (Cursor / Hermes)

| Target | Destination |
|--------|-------------|
| Cursor | `~/.cursor/skills/<skill>/SKILL.md` |
| Hermes all | `~/.hermes/skills/<skill>/SKILL.md` |
| Hermes profile | `$HERMES_HOME/skills/<skill>/SKILL.md` |

| Skill | Source under `~/.ai-pro-skills/` |
|-------|----------------------------------|
| `ai-pro-skills` | `SKILL.md` |
| `coolify` | `coolify/SKILL.md` |
| `zscaler` | `zscaler/SKILL.md` |
| `agent-browser` | `agent-browser/SKILL.md` (+ npm install) |
| `sf` | `SF/SKILL.md` (then `/sf` syncs into `~/.ai-skills/sf-skills`) |
| `google-workspace` | `google-workspace/` (full tree: `SKILL.md`, `scripts/`, `references/`) |
| `powerpoint` | `powerpoint/` (full tree: `SKILL.md`, `scripts/`, `editing.md`, `pptxgenjs.md`, …) |

Use the [install prompt](#-install-prompt-cursor-or-hermes) or `/ai-pro-skills`.

## 🚀 Usage

Invoke via:
- Cursor Agent: `/coolify`, `/zscaler`, `/agent-browser`, `/sf`, `/google-workspace`, `/powerpoint`
- Direct CLI under `~/.ai-pro-skills/<skill>/`
- Hermes cron / shell

For **agent-browser**, after Cursor install, also run once:

```bash
npm i -g agent-browser && agent-browser install
```

Then load workflows with `agent-browser skills get core` (see [`agent-browser/README.md`](agent-browser/README.md)).

For **sf**, after installing the meta-skill, run `/sf` to sync [forcedotcom/sf-skills](https://github.com/forcedotcom/sf-skills.git) into `~/.ai-skills/sf-skills` and copy chosen skills (working dir: `~/.ai-skills/sf-skills/skills/{skills_dir}`).

For **google-workspace**, run setup once (see its `SKILL.md`):

```bash
python ~/.ai-pro-skills/google-workspace/scripts/setup.py --check
```

OAuth files live under `$HERMES_HOME` (`google_token.json`, `google_client_secret.json`) — never commit them.

For **powerpoint**, follow its `SKILL.md` / `editing.md` / `pptxgenjs.md` under `~/.ai-pro-skills/powerpoint`.

---

*Standalone pro skills repo — keep in sync with Cursor via the install prompt.*
