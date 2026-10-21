#!/usr/bin/env python3
"""
Pull a pool of candidate posts from formula1@lemmy.world.

Lemmy's API is public: no account, no key, nothing behind a login. This only
builds a pool to read from — the 200 rows in labels.csv were picked from it by
hand, and data/sources.csv links each one back to its comment.

    python collect.py --out pool.csv

Three kinds of thread, because the community talks differently in each:

    live      [RACE] / [QUALIFYING] / [SPRINT] discussion threads, written
              while the session is on
    post      [POST RACE] threads and "X wins the Y Grand Prix" posts
    news      everything else: articles, quotes, announcements

Comments are kept whole. Dropped: deleted or removed comments, bot accounts,
and anything that is only a link or an image once those are stripped out.
"""

import argparse
import csv
import json
import re
import sys
import time
import urllib.request

API = "https://lemmy.world/api/v3"
COMMUNITY = "formula1@lemmy.world"
HEADERS = {"User-Agent": "takemeter-coursework/0.1 (one-off collection for a class project)"}

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, OSError, ValueError):
        pass


def get(path):
    request = urllib.request.Request(f"{API}/{path}", headers=HEADERS)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def thread_kind(title):
    t = title.upper()
    if "POST RACE" in t or re.search(r"\bWINS THE\b", t):
        return "post"
    if "DISCUSSION THREAD" in t or "SHOOTOUT" in t:
        return "live"
    return "news"


def list_threads(pages):
    threads = {}
    for sort in ("MostComments", "TopAll", "New"):
        for page in range(1, pages + 1):
            data = get(f"post/list?community_name={COMMUNITY}&sort={sort}"
                       f"&limit=50&page={page}&type_=All")
            for view in data["posts"]:
                post = view["post"]
                if view["counts"]["comments"] < 8:
                    continue
                threads[post["id"]] = {
                    "title": post["name"],
                    "kind": thread_kind(post["name"]),
                    "comments": view["counts"]["comments"],
                }
            time.sleep(0.4)
    return threads


def strip_media(text):
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)       # images
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)     # keep link text
    text = re.sub(r"https?://\S+", " ", text)                # bare urls
    return text.strip()


def keep(view):
    comment = view["comment"]
    if comment["deleted"] or comment["removed"] or view["creator"].get("bot_account"):
        return False
    text = comment["content"]
    return 30 <= len(text) <= 1200 and len(strip_media(text)) >= 25


def comments_for(post_id, max_pages):
    out = []
    for page in range(1, max_pages + 1):
        data = get(f"comment/list?post_id={post_id}&sort=Top&limit=50&page={page}&type_=All")
        out.extend(data["comments"])
        if len(data["comments"]) < 50:
            break
        time.sleep(0.4)
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", default="pool.csv")
    parser.add_argument("--per-kind", type=int, default=30,
                        help="threads to read from per kind (default 30)")
    parser.add_argument("--thread-pages", type=int, default=6)
    args = parser.parse_args()

    threads = list_threads(args.thread_pages)
    by_kind = {"live": [], "post": [], "news": []}
    for post_id, info in sorted(threads.items(), key=lambda kv: -kv[1]["comments"]):
        by_kind[info["kind"]].append(post_id)

    rows, seen = [], set()
    for kind, ids in by_kind.items():
        for post_id in ids[: args.per_kind]:
            for view in comments_for(post_id, max_pages=3):
                text = view["comment"]["content"]
                if not keep(view) or text in seen:
                    continue
                seen.add(text)
                rows.append({
                    "kind": kind,
                    "thread": threads[post_id]["title"],
                    "published": view["comment"]["published"][:10],
                    "url": view["comment"]["ap_id"],
                    "text": text,
                })
            time.sleep(0.4)
        print(f"{kind:<5} {len([r for r in rows if r['kind'] == kind])} comments")

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["kind", "thread", "published", "url", "text"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} candidates to {args.out}")


if __name__ == "__main__":
    main()
