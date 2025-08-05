// frontend/quiz-frontend/vue.config.js
const path = require('path');

module.exports = {
  // 1) إخراج البناء إلى مجلد Django frontend_dist/dist
  outputDir: path.resolve(__dirname, '..', '..', 'backend', 'frontend_dist', 'dist'),

  // 2) جميع الموارد (CSS/JS/IMG) توضع في dist/static
  assetsDir: 'static',

  // 3) مسار عام يبدأ بـ /static/ في الإنتاج، و/ في التطوير
  publicPath: process.env.NODE_ENV === 'production'
    ? '/static/'
    : '/',

  // 4) اسم ملف index لا يتغير
  indexPath: 'index.html',
  filenameHashing: false,

  // 5) خادم التطوير يوجّه طلبات /api إلى Django
  devServer: {
    proxy: {
      '^/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
        logLevel: 'debug'
      }
    }
  },

  // 6) إعداد PWA وWorkbox
  pwa: {
    name: 'Quiz App',
    themeColor: '#42b983',
    msTileColor: '#000000',
    workboxPluginMode: 'GenerateSW',
    workboxOptions: {
      swDest: 'service-worker.js',
      clientsClaim: true,
      skipWaiting: true,
      navigateFallback: '/offline.html',
      include: [
        /\.html$/,
        /\.js$/,
        /\.css$/,
        /\.png$/,
        /\.svg$/,
        /manifest\.json$/,
        /offline\.html$/
      ],
      runtimeCaching: [
        {
          // ملف JSON الثابت
          urlPattern: /\/static\/data\/questions\.json/,
          handler: 'StaleWhileRevalidate',
          options: {
            cacheName: 'quiz-data-cache',
            expiration: {
              maxEntries: 50,
              maxAgeSeconds: 24 * 60 * 60
            },
            cacheableResponse: {
              statuses: [0, 200]
            }
          }
        },
        {
          // استدعاؤات API الخاصة بالأسئلة والكتب
          urlPattern: /^\/api\/quiz\/(?:questions|books)(?:\/|$)/,
          handler: 'NetworkFirst',
          options: {
            cacheName: 'api-cache',
            networkTimeoutSeconds: 5,
            cacheableResponse: {
              statuses: [0, 200]
            }
          }
        },
        {
          // استدعاءات استيراد الأسئلة أو الكتب
          urlPattern: /^\/api\/quiz\/import-(?:questions|books)(?:\/|$)/,
          handler: 'NetworkFirst',
          options: {
            cacheName: 'import-cache',
            networkTimeoutSeconds: 5,
            cacheableResponse: {
              statuses: [0, 200]
            }
          }
        },
        {
          // الموارد الثابتة (JS, CSS, صور)
          urlPattern: /\.(?:js|css|png|jpg|jpeg|svg|gif)$/,
          handler: 'CacheFirst',
          options: {
            cacheName: 'static-resources',
            cacheableResponse: {
              statuses: [0, 200]
            }
          }
        }
      ]
    }
  },

  // 7) إنشاء source maps للإنتاج لتسهيل التصحيح
  productionSourceMap: true,

  // 8) ضبط Webpack لإضافة source maps
  configureWebpack: {
    devtool: 'source-map'
  }
};
