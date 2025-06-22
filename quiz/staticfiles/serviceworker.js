// public/serviceworker.js أو مباشرة في الجذر
const CACHE_NAME = 'quiz-pwa-cache-v1';

const urlsToCache = [
  '/',
  '/index.html',
  '/static/css/style.css',
  '/static/js/app.js',
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-512x512.png',
  '/static/sounds/click.mp3',
  '/static/sounds/correct.mp3',
  '/static/sounds/wrong.mp3',
  '/static/sounds/bg-music.mp3',
];

// التثبيت
self.addEventListener('install', (event) => {
  console.log('[SW] Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
      .then(() => self.skipWaiting())
      .catch((err) => console.error('[SW] Cache install failed:', err))
  );
});

// التفعيل
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating...');
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      )
    )
  );
  return self.clients.claim();
});

// التعامل مع الطلبات
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => response || fetch(event.request))
      .catch(() => {
        console.warn('[SW] Fetch failed for:', event.request.url);
      })
  );
});