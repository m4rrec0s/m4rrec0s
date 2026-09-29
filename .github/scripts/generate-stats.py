#!/usr/bin/env python3
import json
import os
import urllib.request
from html import escape

USERNAME = os.environ.get("GITHUB_REPOSITORY_OWNER", "m4rrec0s")
OUT = "profile/stats.svg"

def get_json(url):
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "m4rrec0s-profile-stats"
        },
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)

user = get_json(f"https://api.github.com/users/{USERNAME}")
public_repos = user.get("public_repos", 0)
followers = user.get("followers", 0)
following = user.get("following", 0)
public_gists = user.get("public_gists", 0)

def fmt(value):
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}m".rstrip("0").rstrip(".")
    if value >= 1_000:
        return f"{value / 1_000:.1f}k".rstrip("0").rstrip(".")
    return str(value)

metrics = [
    ("Public Repos", fmt(public_repos)),
    ("Followers", fmt(followers)),
    ("Following", fmt(following)),
    ("Public Gists", fmt(public_gists)),
]

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="495" height="180" viewBox="0 0 495 180" role="img" aria-label="GitHub stats for {escape(USERNAME)}">
  <style>
    .label {{ font: 600 13px 'Segoe UI', Ubuntu, Sans-Serif; fill: #c9d1d9; }}
    .value {{ font: 700 28px 'Segoe UI', Ubuntu, Sans-Serif; fill: #0CF25D; }}
    .title {{ font: 700 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: #0CF25D; }}
    .muted {{ font: 400 11px 'Segoe UI', Ubuntu, Sans-Serif; fill: #8b949e; }}
  </style>
  <rect x="0.5" y="0.5" width="494" height="179" rx="6" fill="#0d1117" stroke="#30363d"/>
  <text x="24" y="34" class="title">GitHub Overview</text>
  <text x="24" y="54" class="muted">@{escape(USERNAME)} · public activity</text>

  <line x1="247.5" y1="72" x2="247.5" y2="154" stroke="#30363d"/>
  <line x1="24" y1="113" x2="471" y2="113" stroke="#21262d"/>

  <text x="24" y="94" class="value">{metrics[0][1]}</text>
  <text x="82" y="92" class="label">{metrics[0][0]}</text>

  <text x="271" y="94" class="value">{metrics[1][1]}</text>
  <text x="329" y="92" class="label">{metrics[1][0]}</text>

  <text x="24" y="144" class="value">{metrics[2][1]}</text>
  <text x="82" y="142" class="label">{metrics[2][0]}</text>

  <text x="271" y="144" class="value">{metrics[3][1]}</text>
  <text x="329" y="142" class="label">{metrics[3][0]}</text>
</svg>
"""

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)

print(f"Wrote {OUT}")
