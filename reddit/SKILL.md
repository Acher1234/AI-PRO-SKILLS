---
name: reddit
description: >-
  Reddit API via PRAW (read/search posts & subreddits, user lookup, post,
  comment, vote, subscribe). Credentials in shared-lib .env. Use when the user
  mentions Reddit, r/, u/, subreddit research, or invokes /reddit_*.
disable-model-invocation: true
---

# reddit

## When to use

Use for Reddit research and engagement. Trigger phrases: "search Reddit",
"what's on r/…", "look up u/…", "post to Reddit", `/reddit_*`.

Primary use: research / intelligence. Confirm with the user before **write**
ops (submit, reply, vote, subscribe).

## Working directory

`~/.ai-pro-skills/reddit`

(Fallback if the library lives under AI-Skills: `~/.ai-skills/AI-PRO-SKILLS/reddit`.)

Registering this skill = copy **only** `SKILL.md` into the tool skills folder
(`~/.cursor/skills/reddit/SKILL.md`, etc.). Do **not** copy the full tree —
CLI + `.env` stay in the shared library (same model as coolify / zscaler).

## Shared environment (see AI-Skills / AI-PRO-SKILLS README)

- **Python**: shared venv — `~/.ai-pro-skills/.venv/bin/python cli.py …`.
  Install deps once from the skill dir:
  `~/.ai-pro-skills/install.sh pip init .` (or `~/.ai-skills/install.sh pip init .`).
  Do **not** create a per-skill `.venv`.
- **Config**: this skill keeps its **own** `.env` in the **shared library**
  folder (`~/.ai-pro-skills/reddit/.env`), next to `cli.py` / `action.py`.
  Never commit secrets.

```bash
cd ~/.ai-pro-skills/reddit
~/.ai-pro-skills/.venv/bin/python cli.py test
```

## Authentication (`.env` in the shared library)

Copy `.env.example` → `.env` under `~/.ai-pro-skills/reddit/`:

```bash
REDDIT_CLIENT_ID=xxx
REDDIT_CLIENT_SECRET=xxx
REDDIT_USERNAME=xxx
REDDIT_PASSWORD=xxx
REDDIT_USER_AGENT=AI-PRO-SKILLS:reddit:1.0 (by u/yourusername)
```

Create a [script app](https://www.reddit.com/prefs/apps) (type **script**) to
get client id/secret. Process env vars override `.env` if set.

## Slash commands

### Setup / account

| Slash | CLI | Description |
|-------|-----|-------------|
| `/reddit_test` | `python cli.py test` | Validate `.env` + auth |
| `/reddit_me` | `python cli.py me` | Authenticated user |

### Read — subreddit / user / search

| Slash | CLI | Description |
|-------|-----|-------------|
| `/reddit_subreddit_info` | `python cli.py subreddit info NAME` | Subreddit info |
| `/reddit_subreddit_posts` | `python cli.py subreddit posts NAME [--sort hot] [--limit N]` | hot/new/top/rising |
| `/reddit_subreddit_search` | `python cli.py subreddit search NAME --query Q` | Search inside subreddit |
| `/reddit_subreddit_rules` | `python cli.py subreddit rules NAME` | Subreddit rules |
| `/reddit_user_info` | `python cli.py user info USERNAME` | User profile |
| `/reddit_user_posts` | `python cli.py user posts USERNAME [--limit N]` | User submissions |
| `/reddit_user_comments` | `python cli.py user comments USERNAME [--limit N]` | User comments |
| `/reddit_search_posts` | `python cli.py search posts QUERY [--subreddit all] [--sort …] [--time-filter …]` | Global search |
| `/reddit_search_subreddits` | `python cli.py search subreddits QUERY` | Find communities |
| `/reddit_post_get` | `python cli.py post get POST_ID` | Post details |
| `/reddit_post_comments` | `python cli.py post comments POST_ID [--limit N] [--sort best]` | Comments |
| `/reddit_discover_popular` | `python cli.py discover popular [--limit N]` | Popular subs |
| `/reddit_discover_default` | `python cli.py discover default [--limit N]` | Default subs |

### Write (confirm with user first)

| Slash | CLI | Description |
|-------|-----|-------------|
| `/reddit_post_submit-text` | `python cli.py post submit-text --subreddit S --title T --body B` | Self post |
| `/reddit_post_submit-link` | `python cli.py post submit-link --subreddit S --title T --url U` | Link post |
| `/reddit_post_reply` | `python cli.py post reply POST_ID --body B` | Top-level comment |
| `/reddit_comment_reply` | `python cli.py comment reply COMMENT_ID --body B` | Nested reply |
| `/reddit_vote_up` | `python cli.py vote up THING_ID` | Upvote (`t3_`/`t1_`) |
| `/reddit_vote_down` | `python cli.py vote down THING_ID` | Downvote |
| `/reddit_vote_clear` | `python cli.py vote clear THING_ID` | Clear vote |
| `/reddit_subscribe_add` | `python cli.py subscribe add NAME` | Join subreddit |
| `/reddit_subscribe_remove` | `python cli.py subscribe remove NAME` | Leave subreddit |

## How to run

1. `cd ~/.ai-pro-skills/reddit`.
2. Ensure `.env` there (from `.env.example`); run `/reddit_test`.
3. Map `/reddit_<…>` → `~/.ai-pro-skills/.venv/bin/python cli.py …`; return JSON.
4. Confirm before any write operation.

### Examples

```bash
python cli.py search posts "Claude AI" --sort relevance --time-filter month --limit 15
python cli.py subreddit info LocalLLaMA
python cli.py subreddit posts LocalLLaMA --sort hot --limit 10
python cli.py user info spez
python cli.py subreddit search learnpython --query PRAW --limit 20
```

## Files (shared library)

```
~/.ai-pro-skills/reddit/
├── SKILL.md           # Source (also registered as a copy into the tool)
├── cli.py
├── action.py
├── _skill_home.py
├── requirements.txt
├── .env.example
├── .env               # local secrets — never commit
└── .gitignore
```

## Notes

- Prefer research/read flows; treat submit/reply/vote as high-impact.
- Strip `r/` / `u/` prefixes before passing names to the CLI.
- Never commit `.env`. Keep secrets out of chat logs when possible.
