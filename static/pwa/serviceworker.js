const CACHE_NAME = 'quiz-pwa-cache-v1';

const urlsToCache = [
  '/',
  '/index.html',
  '/offline.html',
  '/static/css/style.css',
  '/static/js/app.js',
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-512x512.png',
  '/static/sounds/click.mp3',
  '/static/sounds/correct.mp3',
  '/static/sounds/wrong.mp3',
  '/static/sounds/bg-music.mp3',
  '/static/data/questions.json',  // ✅ هذا مهم
];

self.addEventListener('install', (event) => {
  console.log('[SW] Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return Promise.all(
        urlsToCache.map((url) =>
          fetch(url).then((response) => {
            if (!response.ok) {
              throw new Error(`❌ Failed to fetch ${url}: ${response.status}`);
            }
            return cache.put(url, response.clone());
          }).catch((err) => {
            console.error(`[SW] ❌ Error caching ${url}:`, err);
          })
        )
      );
    }).then(() => self.skipWaiting())
  );
});
// ✅ عند التفعيل: حذف الكاش القديم
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

// ✅ عند الطلب: تقديم البيانات من الكاش أو الشبكة، أو صفحة offline.html عند الفشل
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        if (response) {
          return response; // إذا كان هناك استجابة في الكاش، إرجعها
        }
        return fetch(event.request) // حاول جلب البيانات من الشبكة
          .then((networkResponse) => {
            if (!networkResponse || networkResponse.status !== 200) {
              return networkResponse; // إرجاع الاستجابة إذا كانت صحيحة
            }
            // إضافة الاستجابة إلى الكاش (اختياري)
            return caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, networkResponse.clone());
              return networkResponse; // إرجاع الاستجابة
            });
          })
          .catch(() => caches.match('/offline.html')); // إذا فشلت الطلبات، إرجع صفحة عدم الاتصال
      })
  );
});