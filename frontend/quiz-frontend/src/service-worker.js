/// <reference lib="webworker" />
import { precacheAndRoute, cleanupOutdatedCaches } from 'workbox-precaching';
import { registerRoute } from 'workbox-routing';
import { NetworkFirst, CacheFirst, StaleWhileRevalidate } from 'workbox-strategies';
import { CacheableResponsePlugin } from 'workbox-cacheable-response';
import { ExpirationPlugin } from 'workbox-expiration';

// 🧹 تنظيف الكاشات القديمة
cleanupOutdatedCaches();

// 📦 تهيئة الكاش الأساسي من Webpack (precache)
precacheAndRoute(self.__WB_MANIFEST || []);

// 🌐 صفحات SPA - fallback للتنقل
registerRoute(
  ({ request }) => request.mode === 'navigate',
  new NetworkFirst({
    cacheName: 'pages-cache',
    plugins: [
      new CacheableResponsePlugin({ statuses: [0, 200] }),
    ],
  })
);

// 📡 API - أسئلة وكتب (GET)
registerRoute(
  ({ url }) => /^\/api\/quiz\/(questions|books)\/$/.test(url.pathname),
  new NetworkFirst({
    cacheName: 'api-cache',
    networkTimeoutSeconds: 5,
    plugins: [
      new CacheableResponsePlugin({ statuses: [0, 200] }),
      new ExpirationPlugin({ maxAgeSeconds: 60 * 60, maxEntries: 20 }), // 1 ساعة
    ],
  })
);

// 📤 API - استيراد أسئلة وكتب (POST)
registerRoute(
  ({ url, request }) =>
    request.method === 'POST' &&
    /^\/api\/quiz\/import-(questions|books)\/$/.test(url.pathname),
  new NetworkFirst({
    cacheName: 'import-cache',
    networkTimeoutSeconds: 5,
    plugins: [
      new CacheableResponsePlugin({ statuses: [0, 200] }),
    ],
  })
);

// 📁 JSON محلي (backup عند ضعف الإنترنت)
registerRoute(
  ({ url }) => url.pathname === '/static/data/questions.json',
  new StaleWhileRevalidate({
    cacheName: 'quiz-json-cache',
    plugins: [
      new CacheableResponsePlugin({ statuses: [0, 200] }),
      new ExpirationPlugin({
        maxEntries: 1,
        maxAgeSeconds: 24 * 60 * 60, // يوم واحد
      }),
    ],
  })
);

// 🧱 ملفات ثابتة: JS, CSS, صور
registerRoute(
  ({ request }) =>
    ['style', 'script', 'image'].includes(request.destination),
  new CacheFirst({
    cacheName: 'static-assets',
    plugins: [
      new CacheableResponsePlugin({ statuses: [0, 200] }),
      new ExpirationPlugin({
        maxEntries: 50,
        maxAgeSeconds: 7 * 24 * 60 * 60, // أسبوع
      }),
    ],
  })
);

// ⚙️ أحداث التثبيت والتفعيل
self.addEventListener('install', event => {
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  self.clients.claim();
});
