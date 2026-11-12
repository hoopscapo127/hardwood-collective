HARDWOOD COLLECTIVE — HOME-SCREEN APP
=====================================

PUT IT ONLINE (free, about 2 minutes)
1. Go to https://app.netlify.com/drop and sign up (free).
2. Drag this whole "hardwood-collective-app" folder onto the page.
3. Netlify gives you an address like https://something-random.netlify.app
   In Site settings > Change site name, rename it (for example hardwood-collective)
   to get https://hardwood-collective.netlify.app

INSTALL IT ON A PHONE OR COMPUTER
- iPhone / iPad (Safari): open the address, tap Share, then "Add to Home Screen".
- Android (Chrome): open the address, tap "Install app" at the top of the page,
  or the menu (three dots) > "Install app".
- Computer (Chrome or Edge): click "Install app" at the top of the page, or the
  install icon at the right end of the address bar.
After the first visit it works offline.

ADD A NEWS STORY
Open news.json in any text editor and copy one of the entries. Fill in:
  headline     the story's headline
  source       who reported it (NBA.com, ESPN, ...)
  url          link to the original story
  publishedAt  date as YYYY-MM-DD
  team         a team code like "BOS" or "LAL", or null
  postedAt     any number bigger than the newest entry's (it marks the story as new)
Save, then drag the folder onto Netlify again (Deploys tab > drag and drop).
People see the new story, with an alert, the next time they open the app.

AFTER CHANGING ANY OTHER FILE
Open sw.js and change VERSION (for example "hardwood-v1" to "hardwood-v2"),
then redeploy. That tells installed apps to download the new version.

FILES
index.html            the app
players-data.js       every player-season since 1949–50 (from Basketball-Reference.com)
news.json             the News tab
manifest.webmanifest  app name, icon and colors
sw.js                 offline support
icons/, photos/       app icon and Wikimedia Commons photos (credits are in the app footer)
