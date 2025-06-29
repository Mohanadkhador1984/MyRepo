const CACHE_NAME = 'quiz-app-cache-v1';
const urlsToCache = [
  '/',
  '/static/quiz/css/style.css',
  '/static/quiz/js/app.js',
  '/static/quiz/sounds/click.mp3',
  '/static/quiz/sounds/correct.mp3',
  '/static/quiz/sounds/wrong.mp3',
  '/static/quiz/sounds/bg-music.mp3',
  '/static/quiz/data/questions.json',
  '/static/pwa/icons/icon-192x192.png',
  '/static/pwa/icons/icon-512x512.png'
];

// التثبيت
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(urlsToCache);
    })
  );
});

// التفعيل
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) =>
      Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      )
    )
  );
});

// الاسترجاع
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});