#!/usr/bin/env python3
"""Refresh team records and ratings for the Power Rankings tab (standings.json).

Reads the season summary page on Basketball-Reference.com (one request) and writes
each team's wins, losses, margin of victory, SRS and net rating.
Usage: python3 scripts/update_standings.py [season]   (default: season in goat-live.json)
"""
import datetime
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "standings.json")


def season_default():
    try:
        with open(os.path.join(ROOT, "goat-live.json"), encoding="utf-8") as fh:
            return int(json.load(fh)["season"])
    except Exception:
        return 2027


def main():
    season = int(sys.argv[1]) if len(sys.argv) > 1 else season_default()
    url = "https://www.basketball-reference.com/leagues/NBA_%d.html" % season
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; WiseHoops/1.0)"})
    html = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")

    start = html.find('id="advanced-team"')
    if start < 0:
        sys.exit("Couldn't find the team ratings table; the page layout may have changed. Nothing written.")
    end = html.find("</table>", start)
    table = html[start:end]

    teams = []
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", table, re.S):
        cells = dict(re.findall(r'<t[dh][^>]*data-stat="([a-z_0-9]+)"[^>]*>(.*?)</t[dh]>', row, re.S))
        m = re.search(r"/teams/([A-Z]{3})/", cells.get("team", ""))
        if not m:
            continue  # header or league-average row
        name = re.sub(r"<[^>]+>", "", cells["team"]).replace("*", "").strip()

        def num(key):
            try:
                return float(re.sub(r"<[^>]+>", "", cells.get(key, "")).strip() or 0)
            except ValueError:
                return 0.0

        net = num("net_rtg") if "net_rtg" in cells else round(num("off_rtg") - num("def_rtg"), 1)
        teams.append([m.group(1), name, int(num("wins")), int(num("losses")), round(num("mov"), 2), round(num("srs"), 2), round(net, 1)])

    if len(teams) != 30:
        sys.exit("Found %d teams instead of 30; the page layout may have changed. Nothing written." % len(teams))

    teams.sort(key=lambda t: -t[6])
    today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5)))
    # Ratings on the page cover games through the previous night.
    asof = (today - datetime.timedelta(days=1)).strftime("%B %-d, %Y")
    out = {"season": season, "asof": asof, "updated": today.strftime("%Y-%m-%d"),
           "fields": ["code", "name", "W", "L", "MOV", "SRS", "NetRtg"], "teams": teams}

    old = None
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as fh:
            old = json.load(fh)
    if old and old.get("teams") == teams:
        print("No changes to team records.")
        return
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print("Updated standings for %d teams (through games of %s)." % (len(teams), asof))


if __name__ == "__main__":
    main()
