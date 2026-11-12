#!/usr/bin/env python3
"""Refresh this season's win shares for the active players in goat-live.json.

Reads the season's advanced stats page on Basketball-Reference.com (one request),
updates "players" and "updated", and leaves "awards" untouched.
Usage: python3 scripts/update_goat.py
"""
import datetime
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "goat-live.json")


def main():
    with open(PATH, encoding="utf-8") as fh:
        live = json.load(fh)
    season = int(live["season"])
    ids = set(live.get("players", {}).keys())
    url = "https://www.basketball-reference.com/leagues/NBA_%d_advanced.html" % season
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; WiseHoops/1.0)"})
    html = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")

    found = {}
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.S):
        m = re.search(r'data-append-csv="([^"]+)"', row)
        if not m or 'data-stat="name_display"' not in row:
            continue
        pid = m.group(1)
        if pid not in ids or pid in found:  # first row is the season total for traded players
            continue
        cells = {}
        for key, val in re.findall(r'<t[dh][^>]*data-stat="([a-z_0-9]+)"[^>]*>(.*?)</t[dh]>', row, re.S):
            cells[key] = re.sub(r"<[^>]+>", "", val).strip()

        def num(key):
            try:
                return float(cells.get(key) or 0)
            except ValueError:
                return 0.0

        found[pid] = {"g": int(num("games")), "ws": round(num("ws"), 1)}

    if len(found) < len(ids) // 2:
        sys.exit("Only matched %d of %d players; the page layout may have changed. Nothing written." % (len(found), len(ids)))

    changed = False
    for pid, stats in found.items():
        if live["players"].get(pid) != stats:
            live["players"][pid] = stats
            changed = True
    if not changed:
        print("No stat changes (%d players matched)." % len(found))
        return
    live["updated"] = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5))).strftime("%Y-%m-%d")
    with open(PATH, "w", encoding="utf-8") as fh:
        json.dump(live, fh, indent=2)
        fh.write("\n")
    missing = sorted(ids - set(found))
    print("Updated %d players%s." % (len(found), ("; not on the page yet: " + ", ".join(missing)) if missing else ""))


if __name__ == "__main__":
    main()
