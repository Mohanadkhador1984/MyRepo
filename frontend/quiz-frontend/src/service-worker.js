/// <reference lib="webworker" />
import { precacheAndRoute, cleanupOutdatedCaches } from 'workbox-precaching';
import { registerRoute }              from 'workbox-routing';
import {
  NetworkFirst,
  CacheFirst,
  StaleWhileRevalidate
} from 'workbox-strategies';
import { CacheableResponsePlugin } from 'workbox-cacheable-response';
import { ExpirationPlugin }        from 'workbox-expiration';

// 🧹 تنظيف الكاشات القديمة
cleanupOutdatedCaches();

// 📦 تحضير قائمة الـ precache:
//    ندمج هنا ما تضخه Webpack عبر __WB_MANIFEST
//    ثم نضيف ملفات الصوت يدوياً
const ASSETS = [
  ...(self.__WB_MANIFEST || []),
  { url: '/quiz/sounds/click.mp3',    revision: null },
  { url: '/quiz/sounds/correct.mp3',  revision: null },
  { url: '/quiz/sounds/wrong.mp3',    revision: null },
  { url: '/quiz/sounds/bg-music.mp3', revision: null },
];

precacheAndRoute(ASSETS);

// 🌐 صفحات SPA – NetworkFirst مع fallback من الكاش
registerRoute(
  ({ request }) => request.mode === 'navigate',
  new NetworkFirst({
    cacheName: 'pages-cache',
    plugins: [
      new CacheableResponsePlugin({ statuses: [0, 200] })
    ],
  })
);

// 📡 API – GET أسئلة وكتب
registerRoute(
  ({ url, request }) =>
    request.method === 'GET' &&
    /^\/api\/quiz\/(questions|books)\//.test(url.pathname),
  new NetworkFirst({
    cacheName: 'api-cache',
    networkTimeoutSeconds: 5,
    plugins: [
      new CacheableResponsePlugin({ statuses: [0, 200] }),
      new ExpirationPlugin({ maxAgeSeconds: 3600, maxEntries: 20 })
    ],
  })
);

// 📁 JSON محلي
registerRoute(
  ({ url }) => url.pathname.endsWith('/static/data/questions.json'),
  new StaleWhileRevalidate({
    cacheName: 'quiz-json-cache',
    plugins: [
      new CacheableResponsePlugin({ statuses: [0, 200] }),
      new ExpirationPlugin({ maxEntries: 1, maxAgeSeconds: 86400 })
    ],
  })
);

// 🎵 مسار ملفات الصوت – استراتيجية CacheFirst
registerRoute(
  ({ request, url }) =>
    request.destination === 'audio' ||
    url.pathname.startsWith('/quiz/sounds/'),
  new CacheFirst({
    cacheName: 'audio-cache',
    plugins: [
      new CacheableResponsePlugin({ statuses: [0, 200] }),
      // احتفظ بآخر 10 أصوات ما يصل إلى 7 أيام
      new ExpirationPlugin({ maxEntries: 10, maxAgeSeconds: 7 * 24 * 3600 })
    ],
  })
);

// 🧱 ملفات ثابتة أخرى: CSS, JS, الصور
registerRoute(
  ({ request }) => ['style', 'script', 'image', 'font'].includes(request.destination),
  new CacheFirst({
    cacheName: 'static-assets',
    plugins: [
      new CacheableResponsePlugin({ statuses: [0, 200] }),
      new ExpirationPlugin({ maxEntries: 50, maxAgeSeconds: 7 * 24 * 3600 })
    ],
  })
);

// ⚙️ Install & Activate
self.addEventListener('install',  () => self.skipWaiting());
self.addEventListener('activate', () => self.clients.claim());
