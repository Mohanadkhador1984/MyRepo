/// <reference lib="webworker" />

import { precacheAndRoute, cleanupOutdatedCaches } from 'workbox-precaching';
import { registerRoute } from 'workbox-routing';
import {
  NetworkFirst,
  CacheFirst,
  StaleWhileRevalidate
} from 'workbox-strategies';
import { CacheableResponsePlugin } from 'workbox-cacheable-response';
import { ExpirationPlugin } from 'workbox-expiration';

// 🧹 تنظيف الكاشات القديمة
cleanupOutdatedCaches();

// 📦 إعداد قائمة الحفظ المسبق (precaching):
//    ندمج هنا مُدخلات Webpack الذاتية + الصوتيات صراحة
const assetsToPrecache = [
  // المخرجات التي يحقنها Workbox تلقائياً عبر __WB_MANIFEST
  ...(self.__WB_MANIFEST || []),

  // أصوات تطبيق البكالوريا
  { url: '/quiz/sounds/click.mp3',    revision: null },
  { url: '/quiz/sounds/correct.mp3',  revision: null },
  { url: '/quiz/sounds/wrong.mp3',    revision: null },
  { url: '/quiz/sounds/bg-music.mp3', revision: null },
];

// تنفيذ الحفظ المسبق لمرة واحدة
precacheAndRoute(assetsToPrecache);

// 🌐 صفحات SPA - fallback للتنقل
registerRoute(
  ({ request }) => request.mode === 'navigate',
  new NetworkFirst({
    cacheName: 'pages-cache',
    plugins: [
      new CacheableResponsePlugin({ statuses: [0, 200] })
    ],
  })
);

// 📡 API - أسئلة وكتب (GET)
registerRoute(
  ({ url, request }) =>
    request.method === 'GET' &&
    /^\/api\/quiz\/(questions|books)\/$/.test(url.pathname),
  new NetworkFirst({
    cacheName: 'api-cache',
    networkTimeoutSeconds: 5,
    plugins: [
      new CacheableResponsePlugin({ statuses: [0, 200] }),
      new ExpirationPlugin({
        maxAgeSeconds: 60 * 60,     // ساعة
        maxEntries: 20,
      }),
    ],
  })
);

// 📤 API - استيراد (POST)
registerRoute(
  ({ url, request }) =>
    request.method === 'POST' &&
    /^\/api\/quiz\/import-(questions|books)\/$/.test(url.pathname),
  new NetworkFirst({
    cacheName: 'import-cache',
    networkTimeoutSeconds: 5,
    plugins: [
      new CacheableResponsePlugin({ statuses: [0, 200] })
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
        maxAgeSeconds: 24 * 60 * 60, // يوم
      }),
    ],
  })
);

// 🧱 ملفات ثابتة: JS, CSS, صور
registerRoute(
  ({ request }) => ['style', 'script', 'image'].includes(request.destination),
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
self.addEventListener('install', event => self.skipWaiting());
self.addEventListener('activate', event => self.clients.claim());
