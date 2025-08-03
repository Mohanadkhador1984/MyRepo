// src/service-worker.js
import { precacheAndRoute, cleanupOutdatedCaches } from 'workbox-precaching';
import { registerRoute } from 'workbox-routing';
import { NetworkFirst, CacheFirst } from 'workbox-strategies';
import { CacheableResponsePlugin } from 'workbox-cacheable-response';

// تنظيف الكاش القديم
cleanupOutdatedCaches();

// حقن قائمة الأصول
precacheAndRoute(self.__WB_MANIFEST);

// navigation fallback
registerRoute(
  ({ request }) => request.mode === 'navigate',
  new NetworkFirst({ cacheName: 'pages-cache' })
);

// API Questions & Books
registerRoute(
  ({ url }) => url.pathname.match(/^\/api\/quiz\/(questions|books)\/$/),
  new NetworkFirst({
    cacheName: 'api-cache',
    networkTimeoutSeconds: 5,
    plugins: [ new CacheableResponsePlugin({ statuses: [0,200] }) ]
  })
);

// Import endpoints (POST)
registerRoute(
  ({ url }) => url.pathname.match(/^\/api\/quiz\/import-(questions|books)\/$/),
  new NetworkFirst({
    cacheName: 'import-cache',
    networkTimeoutSeconds: 5,
    plugins: [ new CacheableResponsePlugin({ statuses: [0,200] }) ]
  }),
  'POST'
);

// Static assets
registerRoute(
  /\.(?:js|css|png|jpg|jpeg|svg|gif)$/,
  new CacheFirst({
    cacheName: 'static-resources',
    plugins: [ new CacheableResponsePlugin({ statuses: [0,200] }) ]
  })
);

// Install & activate
self.addEventListener('install', event => self.skipWaiting());
self.addEventListener('activate', event => self.clientsClaim());
