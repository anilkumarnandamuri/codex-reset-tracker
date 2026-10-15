#!/usr/bin/env python3
"""Regenerate data/resets.json from X API post JSON (search/timeline response or list of posts).
Usage: python3 scripts/update_resets.py data/raw_posts.json [more.json ...] [-o data/resets.json]
Only posts by @thsottiaux whose text CONFIRMS a delivered global reset are included."""
import json, sys, re
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
PT = ZoneInfo("America/Los_Angeles")
CONFIRM = re.compile(r"reset all propagated|reset in the bag|it's done|the reset has been|loading a banked reset|we'll reset usage limits|we’ll reset usage limits|done and dusted", re.I)
AUTHOR_ID = "1953337039510003712"

def load(paths):
    posts = {}
    for p in paths:
        d = json.load(open(p))
        items = d if isinstance(d, list) else d.get("data", []) + d.get("includes", {}).get("tweets", [])
        for t in items:
            posts[t["id"]] = t
    return posts

def build(posts):
    out = []
    for t in posts.values():
        if t.get("author_id", AUTHOR_ID) != AUTHOR_ID or not CONFIRM.search(t["text"]):
            continue
        if "reset" not in t["text"].lower():
            # short confirmations ("Done and dusted") count only if they quote/reply to a reset thread
            chain, cur = [], t
            for _ in range(3):
                refs = [posts.get(r["id"]) for r in cur.get("referenced_tweets", []) if r["type"] in ("quoted", "replied_to")]
                cur = next((q for q in refs if q), None)
                if not cur: break
                chain.append(cur)
            if not any("reset" in q["text"].lower() for q in chain):
                continue
        dt = datetime.fromisoformat(t["created_at"].replace("Z", "+00:00"))
        ann = None
        for r in t.get("referenced_tweets", []):
            q = posts.get(r["id"])
            if q and ("reset" in q["text"].lower() or any("reset" in (posts.get(r2["id"]) or {}).get("text", "").lower() for r2 in q.get("referenced_tweets", []) if r2["type"] == "replied_to")):
                ann = {"id": q["id"], "url": f"https://x.com/thsottiaux/status/{q['id']}", "text": q["text"][:200]}
                # walk to thread root e.g. "Day 8/ Reset"
                for r2 in q.get("referenced_tweets", []):
                    q2 = posts.get(r2["id"])
                    if q2 and r2["type"] == "replied_to" and "reset" in q2["text"].lower():
                        ann["root_text"] = q2["text"][:200]
        text = re.sub(r"\s*https://t\.co/\S+$", "", t["text"]).strip()
        out.append({
            "id": t["id"], "utc": dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "pt": dt.astimezone(PT).strftime("%Y-%m-%d %I:%M %p %Z"),
            "url": f"https://x.com/thsottiaux/status/{t['id']}",
            "quote": text[:280], "status": "announced" if re.search(r"we.ll reset", t["text"], re.I) else "confirmed", "announcement": ann})
    out.sort(key=lambda r: r["utc"], reverse=True)
    return out

if __name__ == "__main__":
    a = sys.argv[1:]; o = "data/resets.json"
    if "-o" in a: i = a.index("-o"); o = a[i+1]; del a[i:i+2]
    res = build(load(a or ["data/raw_posts.json"]))
    json.dump({"source": "@thsottiaux on X", "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               "resets": res}, open(o, "w"), indent=2, ensure_ascii=False)
    print(f"wrote {len(res)} resets to {o}")
