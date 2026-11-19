// WiseHoops offline support.
// When you change any file, bump VERSION so installed apps pick up the update.
const VERSION = "wisehoops-v6";
const CORE = [
  "./", "index.html", "players-data.js", "manifest.webmanifest", "news.json", "goat-live.json", "standings.json",
  "icons/icon-180.png", "icons/icon-192.png", "icons/icon-512.png",
  "photos/lebron.jpg", "photos/curry.jpg", "photos/magic.jpg", "photos/giannis.jpg", "photos/kobe.jpg",
  "photos/jokic.jpg", "photos/durant.jpg", "photos/luka.jpg", "photos/hawks.jpg", "photos/celtics.jpg",
];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== VERSION).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);

  // News and GOAT stats: always try for the latest, fall back to the saved copy offline.
  const live = ["/news.json", "/goat-live.json", "/standings.json"].find(p => url.pathname.endsWith(p));
  if (url.origin === location.origin && live) {
    const key = live.slice(1);
    e.respondWith(fetch(req).then(res => { const copy = res.clone(); caches.open(VERSION).then(c => c.put(key, copy)); return res; })
      .catch(() => caches.match(key)));
    return;
  }

  // Google Fonts: serve the saved copy, refresh it in the background.
  if (url.hostname === "fonts.googleapis.com" || url.hostname === "fonts.gstatic.com") {
    e.respondWith(caches.open(VERSION).then(async c => {
      const hit = await c.match(req);
      const net = fetch(req).then(res => { c.put(req, res.clone()); return res; }).catch(() => hit);
      return hit || net;
    }));
    return;
  }

  // Everything else from this site: saved copy first, then the network.
  if (url.origin === location.origin) {
    e.respondWith(caches.match(req, { ignoreSearch: true }).then(hit => hit || fetch(req).then(res => {
      if (res.ok) { const copy = res.clone(); caches.open(VERSION).then(c => c.put(req, copy)); }
      return res;
    }).catch(() => caches.match("index.html"))));
  }
});
