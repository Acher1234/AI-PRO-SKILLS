# fathom — Fathom meeting fetcher

Fetches meetings, transcripts, AI summaries, and action items from the Fathom API via a bundled Python CLI. Adapted for AI-PRO-SKILLS from [glebis/claude-skills · fathom](https://github.com/glebis/claude-skills/tree/431ff86f7530c2223855666b9e97ccdb7e95fca7/fathom): same scripts, but **shared code** + a **per-workspace `.env` resolved by location** through `common/skill_home.py`.

## Install this skill

Copy the folder (or at least `SKILL.md` + `scripts/`) to:

- Cursor: `~/.cursor/skills/fathom/`
- Hermes: `~/.hermes/skills/fathom/` or `$HERMES_HOME/skills/fathom/`

Then install deps and set credentials:

```bash
cd ~/.cursor/skills/fathom            # your chosen destination
bash install.sh pip init fathom       # or: pip install -r requirements.txt
cp .env.example .env                  # then edit: FATHOM_API_KEY=...
```

## Credentials — `.env` by location

`FATHOM_API_KEY` lives next to the registered skill (not shared), resolved via `common/skill_home.py` (`SkillHome("fathom")`):

| Scope | `.env` path |
|-------|-------------|
| Cursor — this project | `./.cursor/skills/fathom/.env` |
| Cursor — global | `~/.cursor/skills/fathom/.env` |
| Workspace root (fallback) | `./.env` |
| Hermes — this profile | `${HERMES_HOME}/skills/fathom/.env` |
| Override | `FATHOM_ENV_PATH=/path/to/.env` |

Print the resolved path:

```bash
python3 scripts/_skill_home.py
```

## Usage

```bash
python scripts/fetch.py --list                 # recent meetings
python scripts/fetch.py --today                # today's meetings
python scripts/fetch.py --since 2025-01-01     # since a date
python scripts/fetch.py --id abc123            # specific meeting
python scripts/fetch.py --id abc123 --download-video
```

## Files

| File | Role |
|------|------|
| `SKILL.md` | Skill instructions for agents |
| `scripts/fetch.py` | CLI (list / get / today / since) |
| `scripts/utils.py` | Fathom API client + markdown formatting (loads `.env` via shared skill_home) |
| `scripts/download_video.py` | HLS → MP4 downloader (ffmpeg) |
| `scripts/_skill_home.py` | Resolves shared lib + `.env`; prints the `.env` path when run |
| `.env.example` | Template for `FATHOM_API_KEY` |
| `requirements.txt` | Python dependencies |

## Upstream

- [glebis/claude-skills](https://github.com/glebis/claude-skills/tree/431ff86f7530c2223855666b9e97ccdb7e95fca7/fathom)
