WISEHOOPS — HOME-SCREEN APP
===========================

WHERE IT LIVES
The live site is https://wisehoops.netlify.app
It is published from the GitHub repository hoopscapo127/hardwood-collective.
Netlify republishes automatically whenever a file there changes.
Do NOT drag this folder onto Netlify: that would replace the stories and
stats the automatic agent has added on GitHub.

INSTALL IT ON A PHONE OR COMPUTER
- iPhone / iPad (Safari): open the address, tap Share, then "Add to Home Screen".
- Android (Chrome): open the address, tap "Install app" at the top of the page,
  or the menu (three dots) > "Install app".
- Computer (Chrome or Edge): click "Install app" at the top of the page, or the
  install icon at the right end of the address bar.
After the first visit it works offline.

NEWS AND GOAT STATS
A cloud agent ("Hardwood Collective news + GOAT stats" at claude.ai/code/routines)
runs at 8 am and 8 pm Eastern. It adds news stories to news.json and refreshes
this season's stats in goat-live.json, then saves them to GitHub.

CHANGING THE SITE ITSELF
Upload the changed files on GitHub (Add file > Upload files), never news.json.
After changing any file other than news.json or goat-live.json, open sw.js and
change VERSION (for example "wisehoops-v4" to "wisehoops-v5"). That tells
installed apps to download the new version.

FILES
index.html            the app
players-data.js       every player-season since 1949–50 (from Basketball-Reference.com)
news.json             the News tab (updated automatically)
goat-live.json        this season's stats for the GOAT 100 tab (updated automatically)
standings.json        team records for the Power Rankings tab (scripts/update_standings.py)
awards.json           award odds for the Awards tab (scripts/update_awards.py)
scripts/              the script that refreshes goat-live.json
manifest.webmanifest  app name, icon and colors
sw.js                 offline support
icons/, photos/       app icon and Wikimedia Commons photos (credits are in the app footer)
