#!/usr/bin/env python3
"""Hermes / Cursor CLI — Reddit via PRAW (credentials in skill-dir .env)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Skill root on sys.path so ``action`` / ``_skill_home`` import cleanly.
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from _skill_home import display_skill_home, env_path  # noqa: E402
from action import RedditClient  # noqa: E402


def _print_json(data: Any) -> None:
    print(json.dumps(data, indent=2, default=str))


def cmd_test(_: argparse.Namespace) -> int:
    """Validate .env + authenticated identity."""
    client = RedditClient()
    me = client.get_me()
    _print_json({"ok": True, "env": str(env_path()), "me": me})
    return 0


def cmd_me(_: argparse.Namespace) -> int:
    _print_json(RedditClient().get_me())
    return 0


def cmd_subreddit(args: argparse.Namespace) -> int:
    client = RedditClient()
    if args.action == "info":
        _print_json(client.get_subreddit(args.name))
    elif args.action == "posts":
        _print_json(
            client.get_subreddit_posts(
                args.name,
                sort=args.sort,
                limit=args.limit,
                time_filter=args.time_filter,
            )
        )
    elif args.action == "search":
        if not args.query:
            raise ValueError("--query requis pour subreddit search")
        _print_json(
            client.search_subreddit(
                args.name, args.query, sort=args.sort, limit=args.limit
            )
        )
    elif args.action == "rules":
        _print_json(client.get_subreddit_rules(args.name))
    else:
        raise ValueError(f"Action subreddit inconnue: {args.action}")
    return 0


def cmd_user(args: argparse.Namespace) -> int:
    client = RedditClient()
    if args.action == "info":
        _print_json(client.get_user(args.username))
    elif args.action == "posts":
        _print_json(client.get_user_posts(args.username, limit=args.limit))
    elif args.action == "comments":
        _print_json(client.get_user_comments(args.username, limit=args.limit))
    else:
        raise ValueError(f"Action user inconnue: {args.action}")
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    client = RedditClient()
    if args.action == "posts":
        _print_json(
            client.search_posts(
                args.query,
                subreddit=args.subreddit or "all",
                sort=args.sort,
                time_filter=args.time_filter,
                limit=args.limit,
            )
        )
    elif args.action == "subreddits":
        _print_json(client.search_subreddits(args.query, limit=args.limit))
    else:
        raise ValueError(f"Action search inconnue: {args.action}")
    return 0


def cmd_post(args: argparse.Namespace) -> int:
    client = RedditClient()
    if args.action == "get":
        _print_json(client.get_post(args.post_id))
    elif args.action == "comments":
        _print_json(
            client.get_post_comments(
                args.post_id, limit=args.limit, sort=args.sort
            )
        )
    elif args.action == "submit-text":
        if not args.subreddit or not args.title or args.body is None:
            raise ValueError("--subreddit, --title et --body requis")
        _print_json(
            client.submit_text_post(
                args.subreddit, args.title, args.body, flair_id=args.flair_id
            )
        )
    elif args.action == "submit-link":
        if not args.subreddit or not args.title or not args.url:
            raise ValueError("--subreddit, --title et --url requis")
        _print_json(
            client.submit_link_post(
                args.subreddit, args.title, args.url, flair_id=args.flair_id
            )
        )
    elif args.action == "reply":
        if not args.body:
            raise ValueError("--body requis")
        _print_json(client.reply_to_post(args.post_id, args.body))
    else:
        raise ValueError(f"Action post inconnue: {args.action}")
    return 0


def cmd_comment(args: argparse.Namespace) -> int:
    if args.action != "reply":
        raise ValueError(f"Action comment inconnue: {args.action}")
    if not args.body:
        raise ValueError("--body requis")
    _print_json(RedditClient().reply_to_comment(args.comment_id, args.body))
    return 0


def cmd_vote(args: argparse.Namespace) -> int:
    client = RedditClient()
    if args.action == "up":
        client.upvote(args.thing_id)
    elif args.action == "down":
        client.downvote(args.thing_id)
    elif args.action == "clear":
        client.clear_vote(args.thing_id)
    else:
        raise ValueError(f"Action vote inconnue: {args.action}")
    _print_json({"ok": True, "action": args.action, "thing_id": args.thing_id})
    return 0


def cmd_subscribe(args: argparse.Namespace) -> int:
    client = RedditClient()
    if args.action == "add":
        client.subscribe(args.name)
    elif args.action == "remove":
        client.unsubscribe(args.name)
    else:
        raise ValueError(f"Action subscribe inconnue: {args.action}")
    _print_json({"ok": True, "action": args.action, "subreddit": args.name})
    return 0


def cmd_discover(args: argparse.Namespace) -> int:
    client = RedditClient()
    if args.action == "popular":
        _print_json(client.get_popular_subreddits(limit=args.limit))
    elif args.action == "default":
        _print_json(client.get_default_subreddits(limit=args.limit))
    else:
        raise ValueError(f"Action discover inconnue: {args.action}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="reddit",
        description=(
            f"Reddit CLI (PRAW). Credentials: {display_skill_home()}/.env"
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_test = sub.add_parser("test", help="Validate .env + auth")
    p_test.set_defaults(func=cmd_test)

    p_me = sub.add_parser("me", help="Authenticated user info")
    p_me.set_defaults(func=cmd_me)

    p_sub = sub.add_parser("subreddit", help="Subreddit operations")
    p_sub.add_argument(
        "action", choices=["info", "posts", "search", "rules"]
    )
    p_sub.add_argument("name", help="Subreddit name (without r/)")
    p_sub.add_argument("--query", default=None, help="Search query (search)")
    p_sub.add_argument(
        "--sort",
        default="hot",
        help="posts: hot|new|top|rising|controversial; search: relevance|…",
    )
    p_sub.add_argument("--limit", type=int, default=10)
    p_sub.add_argument(
        "--time-filter",
        default="all",
        dest="time_filter",
        help="For top/controversial: hour|day|week|month|year|all",
    )
    p_sub.set_defaults(func=cmd_subreddit)

    p_user = sub.add_parser("user", help="User operations")
    p_user.add_argument("action", choices=["info", "posts", "comments"])
    p_user.add_argument("username", help="Username (without u/)")
    p_user.add_argument("--limit", type=int, default=10)
    p_user.set_defaults(func=cmd_user)

    p_search = sub.add_parser("search", help="Global search")
    p_search.add_argument("action", choices=["posts", "subreddits"])
    p_search.add_argument("query", help="Search query")
    p_search.add_argument(
        "--subreddit", default="all", help="Limit posts search (default: all)"
    )
    p_search.add_argument("--sort", default="relevance")
    p_search.add_argument(
        "--time-filter", default="all", dest="time_filter"
    )
    p_search.add_argument("--limit", type=int, default=25)
    p_search.set_defaults(func=cmd_search)

    p_post = sub.add_parser("post", help="Post read / write")
    p_post.add_argument(
        "action",
        choices=["get", "comments", "submit-text", "submit-link", "reply"],
    )
    p_post.add_argument(
        "post_id",
        nargs="?",
        default=None,
        help="Post ID (get/comments/reply)",
    )
    p_post.add_argument("--subreddit", default=None)
    p_post.add_argument("--title", default=None)
    p_post.add_argument("--body", default=None)
    p_post.add_argument("--url", default=None)
    p_post.add_argument("--flair-id", default=None, dest="flair_id")
    p_post.add_argument("--limit", type=int, default=20)
    p_post.add_argument("--sort", default="best")
    p_post.set_defaults(func=cmd_post)

    p_comment = sub.add_parser("comment", help="Comment write")
    p_comment.add_argument("action", choices=["reply"])
    p_comment.add_argument("comment_id", help="Comment ID")
    p_comment.add_argument("--body", required=True)
    p_comment.set_defaults(func=cmd_comment)

    p_vote = sub.add_parser("vote", help="Vote on post/comment")
    p_vote.add_argument("action", choices=["up", "down", "clear"])
    p_vote.add_argument("thing_id", help="t3_… (post) or t1_… (comment)")
    p_vote.set_defaults(func=cmd_vote)

    p_subsc = sub.add_parser("subscribe", help="Subscribe / unsubscribe")
    p_subsc.add_argument("action", choices=["add", "remove"])
    p_subsc.add_argument("name", help="Subreddit name")
    p_subsc.set_defaults(func=cmd_subscribe)

    p_disc = sub.add_parser("discover", help="Popular / default subreddits")
    p_disc.add_argument("action", choices=["popular", "default"])
    p_disc.add_argument("--limit", type=int, default=25)
    p_disc.set_defaults(func=cmd_discover)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "post" and args.action in (
            "get",
            "comments",
            "reply",
        ):
            if not args.post_id:
                raise ValueError("post_id requis pour get/comments/reply")
        return args.func(args)
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        return 130
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
