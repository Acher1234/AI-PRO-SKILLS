#!/usr/bin/env python3
"""Reddit API client wrapper (PRAW).

Credentials are loaded from ``.env`` next to this skill's ``SKILL.md``.

Usage:
    from action import RedditClient

    client = RedditClient()
    print(client.get_subreddit("python"))
"""

from __future__ import annotations

from typing import Optional

from _skill_home import display_env_path, display_skill_home, env_path

CREDENTIALS_PATH = env_path()  # resolved at import; prefer env_path() at call time
REQUIRED_KEYS = (
    "REDDIT_CLIENT_ID",
    "REDDIT_CLIENT_SECRET",
    "REDDIT_USERNAME",
    "REDDIT_PASSWORD",
    "REDDIT_USER_AGENT",
)


class RedditClient:
    """High-level wrapper for Reddit API operations via PRAW."""

    def __init__(self):
        self._reddit = None
        self._creds = self._load_credentials()

    def _load_credentials(self) -> dict:
        """Load credentials from the resolved per-workspace ``.env``."""
        path = env_path()
        if not path.exists():
            raise FileNotFoundError(
                f"Credentials not found at {path}. "
                f"Create {display_env_path()} from the skill's .env.example "
                f"(CLI library: {display_skill_home()}) with "
                + ", ".join(REQUIRED_KEYS)
            )

        creds: dict[str, str] = {}
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip().strip("'").strip('"')
            if key.startswith("export "):
                key = key[len("export ") :].strip()
            if key:
                creds[key] = val

        missing = [k for k in REQUIRED_KEYS if not creds.get(k)]
        if missing:
            raise ValueError(
                f"Missing keys in {path}: {', '.join(missing)}"
            )
        return creds

    @property
    def reddit(self):
        """Lazy-load authenticated PRAW instance."""
        if self._reddit is None:
            import praw

            self._reddit = praw.Reddit(
                client_id=self._creds["REDDIT_CLIENT_ID"],
                client_secret=self._creds["REDDIT_CLIENT_SECRET"],
                username=self._creds["REDDIT_USERNAME"],
                password=self._creds["REDDIT_PASSWORD"],
                user_agent=self._creds["REDDIT_USER_AGENT"],
            )
        return self._reddit

    # =========================================================================
    # Account
    # =========================================================================

    def get_me(self) -> dict:
        """Get current authenticated user info."""
        me = self.reddit.user.me()
        return {
            "name": me.name,
            "link_karma": me.link_karma,
            "comment_karma": me.comment_karma,
            "created_utc": me.created_utc,
            "is_gold": me.is_gold,
            "is_mod": me.is_mod,
            "has_verified_email": me.has_verified_email,
        }

    # =========================================================================
    # Subreddit Operations
    # =========================================================================

    def get_subreddit(self, name: str) -> dict:
        """
        Get subreddit information.

        Args:
            name: Subreddit name (without r/ prefix)

        Returns dict with: name, title, description, subscribers, etc.
        """
        sub = self.reddit.subreddit(name)
        return {
            "name": sub.display_name,
            "title": sub.title,
            "description": sub.public_description,
            "description_full": sub.description[:500] if sub.description else None,
            "subscribers": sub.subscribers,
            "created_utc": sub.created_utc,
            "over18": sub.over18,
            "url": f"https://reddit.com/r/{sub.display_name}",
        }

    def get_subreddit_posts(
        self,
        name: str,
        sort: str = "hot",
        limit: int = 10,
        time_filter: str = "all"
    ) -> list[dict]:
        """
        Get posts from a subreddit.

        Args:
            name: Subreddit name
            sort: hot, new, top, rising, controversial
            limit: Number of posts (max 100)
            time_filter: For top/controversial: hour, day, week, month, year, all

        Returns list of posts.
        """
        sub = self.reddit.subreddit(name)
        limit = min(limit, 100)

        if sort == "hot":
            posts = sub.hot(limit=limit)
        elif sort == "new":
            posts = sub.new(limit=limit)
        elif sort == "top":
            posts = sub.top(time_filter=time_filter, limit=limit)
        elif sort == "rising":
            posts = sub.rising(limit=limit)
        elif sort == "controversial":
            posts = sub.controversial(time_filter=time_filter, limit=limit)
        else:
            posts = sub.hot(limit=limit)

        return [self._post_to_dict(p) for p in posts]

    def search_subreddit(
        self,
        name: str,
        query: str,
        sort: str = "relevance",
        limit: int = 10
    ) -> list[dict]:
        """
        Search within a specific subreddit.

        Args:
            name: Subreddit name
            query: Search query
            sort: relevance, hot, top, new, comments
            limit: Number of results

        Returns list of matching posts.
        """
        sub = self.reddit.subreddit(name)
        results = sub.search(query, sort=sort, limit=limit)
        return [self._post_to_dict(p) for p in results]

    def get_subreddit_rules(self, name: str) -> list[dict]:
        """Get subreddit rules."""
        sub = self.reddit.subreddit(name)
        rules = []
        for rule in sub.rules:
            rules.append({
                "short_name": rule.short_name,
                "description": rule.description,
                "kind": rule.kind,
            })
        return rules

    # =========================================================================
    # User Operations
    # =========================================================================

    def get_user(self, username: str) -> dict:
        """
        Get user profile information.

        Args:
            username: Reddit username (without u/ prefix)

        Returns dict with: name, karma, account age, etc.
        """
        user = self.reddit.redditor(username)
        return {
            "name": user.name,
            "link_karma": user.link_karma,
            "comment_karma": user.comment_karma,
            "total_karma": user.link_karma + user.comment_karma,
            "created_utc": user.created_utc,
            "is_gold": user.is_gold,
            "is_mod": user.is_mod,
            "is_employee": user.is_employee,
            "has_verified_email": user.has_verified_email,
            "url": f"https://reddit.com/u/{user.name}",
        }

    def get_user_posts(self, username: str, limit: int = 10) -> list[dict]:
        """Get a user's recent submissions."""
        user = self.reddit.redditor(username)
        posts = user.submissions.new(limit=limit)
        return [self._post_to_dict(p) for p in posts]

    def get_user_comments(self, username: str, limit: int = 10) -> list[dict]:
        """Get a user's recent comments."""
        user = self.reddit.redditor(username)
        comments = user.comments.new(limit=limit)
        return [self._comment_to_dict(c) for c in comments]

    # =========================================================================
    # Search Operations
    # =========================================================================

    def search_posts(
        self,
        query: str,
        subreddit: str = "all",
        sort: str = "relevance",
        time_filter: str = "all",
        limit: int = 25
    ) -> list[dict]:
        """
        Search for posts across Reddit.

        Args:
            query: Search query
            subreddit: Limit to specific subreddit or "all"
            sort: relevance, hot, top, new, comments
            time_filter: hour, day, week, month, year, all
            limit: Number of results

        Returns list of matching posts.
        """
        sub = self.reddit.subreddit(subreddit)
        results = sub.search(query, sort=sort, time_filter=time_filter, limit=limit)
        return [self._post_to_dict(p) for p in results]

    def search_subreddits(self, query: str, limit: int = 10) -> list[dict]:
        """
        Search for subreddits by name/topic.

        Args:
            query: Search query
            limit: Number of results

        Returns list of matching subreddits.
        """
        results = self.reddit.subreddits.search(query, limit=limit)
        subs = []
        for sub in results:
            subs.append({
                "name": sub.display_name,
                "title": sub.title,
                "description": sub.public_description[:200] if sub.public_description else None,
                "subscribers": sub.subscribers,
                "over18": sub.over18,
                "url": f"https://reddit.com/r/{sub.display_name}",
            })
        return subs

    # =========================================================================
    # Post/Comment Operations
    # =========================================================================

    def get_post(self, post_id: str) -> dict:
        """
        Get full post details.

        Args:
            post_id: Post ID (e.g., "abc123" or "t3_abc123")

        Returns post details.
        """
        if post_id.startswith("t3_"):
            post_id = post_id[3:]
        submission = self.reddit.submission(id=post_id)
        return self._post_to_dict(submission, include_body=True)

    def get_post_comments(
        self,
        post_id: str,
        limit: int = 20,
        sort: str = "best"
    ) -> list[dict]:
        """
        Get comments on a post.

        Args:
            post_id: Post ID
            limit: Number of top-level comments
            sort: best, top, new, controversial, old, q&a

        Returns list of comments (flattened).
        """
        if post_id.startswith("t3_"):
            post_id = post_id[3:]

        submission = self.reddit.submission(id=post_id)
        submission.comment_sort = sort
        submission.comments.replace_more(limit=0)  # Skip "more comments" links

        comments = []
        for comment in submission.comments[:limit]:
            comments.append(self._comment_to_dict(comment))
        return comments

    # =========================================================================
    # Discovery
    # =========================================================================

    def get_popular_subreddits(self, limit: int = 25) -> list[dict]:
        """Get popular subreddits."""
        subs = []
        for sub in self.reddit.subreddits.popular(limit=limit):
            subs.append({
                "name": sub.display_name,
                "title": sub.title,
                "subscribers": sub.subscribers,
                "url": f"https://reddit.com/r/{sub.display_name}",
            })
        return subs

    def get_default_subreddits(self, limit: int = 25) -> list[dict]:
        """Get default subreddits."""
        subs = []
        for sub in self.reddit.subreddits.default(limit=limit):
            subs.append({
                "name": sub.display_name,
                "title": sub.title,
                "subscribers": sub.subscribers,
                "url": f"https://reddit.com/r/{sub.display_name}",
            })
        return subs

    # =========================================================================
    # Write Operations
    # =========================================================================

    def submit_text_post(
        self,
        subreddit: str,
        title: str,
        body: str,
        flair_id: Optional[str] = None
    ) -> dict:
        """
        Create a text (self) post.

        Args:
            subreddit: Subreddit name
            title: Post title
            body: Post body (markdown)
            flair_id: Optional flair ID

        Returns created post info.
        """
        sub = self.reddit.subreddit(subreddit)
        submission = sub.submit(title=title, selftext=body, flair_id=flair_id)
        return {
            "id": submission.id,
            "url": submission.url,
            "title": submission.title,
            "subreddit": subreddit,
        }

    def submit_link_post(
        self,
        subreddit: str,
        title: str,
        url: str,
        flair_id: Optional[str] = None
    ) -> dict:
        """
        Create a link post.

        Args:
            subreddit: Subreddit name
            title: Post title
            url: Link URL
            flair_id: Optional flair ID

        Returns created post info.
        """
        sub = self.reddit.subreddit(subreddit)
        submission = sub.submit(title=title, url=url, flair_id=flair_id)
        return {
            "id": submission.id,
            "url": submission.url,
            "title": submission.title,
            "subreddit": subreddit,
        }

    def reply_to_post(self, post_id: str, body: str) -> dict:
        """
        Comment on a post.

        Args:
            post_id: Post ID
            body: Comment text (markdown)

        Returns created comment info.
        """
        if post_id.startswith("t3_"):
            post_id = post_id[3:]
        submission = self.reddit.submission(id=post_id)
        comment = submission.reply(body)
        return {
            "id": comment.id,
            "body": comment.body,
            "url": f"https://reddit.com{comment.permalink}",
        }

    def reply_to_comment(self, comment_id: str, body: str) -> dict:
        """
        Reply to a comment.

        Args:
            comment_id: Comment ID
            body: Reply text (markdown)

        Returns created comment info.
        """
        if comment_id.startswith("t1_"):
            comment_id = comment_id[3:]
        comment = self.reddit.comment(id=comment_id)
        reply = comment.reply(body)
        return {
            "id": reply.id,
            "body": reply.body,
            "url": f"https://reddit.com{reply.permalink}",
        }

    # =========================================================================
    # Voting
    # =========================================================================

    def upvote(self, thing_id: str) -> bool:
        """
        Upvote a post or comment.

        Args:
            thing_id: Full ID (t3_xxx for post, t1_xxx for comment)

        Returns True if successful.
        """
        if thing_id.startswith("t3_"):
            self.reddit.submission(id=thing_id[3:]).upvote()
        elif thing_id.startswith("t1_"):
            self.reddit.comment(id=thing_id[3:]).upvote()
        else:
            # Assume post if no prefix
            self.reddit.submission(id=thing_id).upvote()
        return True

    def downvote(self, thing_id: str) -> bool:
        """Downvote a post or comment."""
        if thing_id.startswith("t3_"):
            self.reddit.submission(id=thing_id[3:]).downvote()
        elif thing_id.startswith("t1_"):
            self.reddit.comment(id=thing_id[3:]).downvote()
        else:
            self.reddit.submission(id=thing_id).downvote()
        return True

    def clear_vote(self, thing_id: str) -> bool:
        """Remove vote from a post or comment."""
        if thing_id.startswith("t3_"):
            self.reddit.submission(id=thing_id[3:]).clear_vote()
        elif thing_id.startswith("t1_"):
            self.reddit.comment(id=thing_id[3:]).clear_vote()
        else:
            self.reddit.submission(id=thing_id).clear_vote()
        return True

    # =========================================================================
    # Subscription
    # =========================================================================

    def subscribe(self, subreddit: str) -> bool:
        """Subscribe to a subreddit."""
        self.reddit.subreddit(subreddit).subscribe()
        return True

    def unsubscribe(self, subreddit: str) -> bool:
        """Unsubscribe from a subreddit."""
        self.reddit.subreddit(subreddit).unsubscribe()
        return True

    # =========================================================================
    # Helpers
    # =========================================================================

    def _post_to_dict(self, post, include_body: bool = False) -> dict:
        """Convert PRAW Submission to dict."""
        result = {
            "id": post.id,
            "title": post.title,
            "author": str(post.author) if post.author else "[deleted]",
            "subreddit": post.subreddit.display_name,
            "score": post.score,
            "upvote_ratio": post.upvote_ratio,
            "num_comments": post.num_comments,
            "created_utc": post.created_utc,
            "url": post.url,
            "permalink": f"https://reddit.com{post.permalink}",
            "is_self": post.is_self,
            "over_18": post.over_18,
            "stickied": post.stickied,
        }
        if include_body and post.is_self:
            result["body"] = post.selftext
        return result

    def _comment_to_dict(self, comment) -> dict:
        """Convert PRAW Comment to dict."""
        return {
            "id": comment.id,
            "author": str(comment.author) if comment.author else "[deleted]",
            "body": comment.body,
            "score": comment.score,
            "created_utc": comment.created_utc,
            "permalink": f"https://reddit.com{comment.permalink}",
            "is_submitter": comment.is_submitter,
            "subreddit": comment.subreddit.display_name if hasattr(comment, 'subreddit') else None,
        }


if __name__ == "__main__":
    # Full CLI lives in cli.py
    from cli import main

    sys.exit(main())