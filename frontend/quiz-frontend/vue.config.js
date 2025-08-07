// frontend/quiz-frontend/vue.config.js
const path = require('path');

module.exports = {
  // 1) إخراج البناء إلى مجلد Django frontend_dist/dist
  outputDir: path.resolve(__dirname, '..', '..', 'backend', 'frontend_dist', 'dist'),

  // 2) جميع الموارد (CSS/JS/IMG) توضع في dist/static
  assetsDir: 'static',

  // 3) مسار عام يبدأ بـ /static/ في الإنتاج، و/ في التطوير
  publicPath: process.env.NODE_ENV === 'production' ? '/static/' : '/',

  // 4) اسم ملف index ثابت وبدون هاش
  indexPath: 'index.html',
  filenameHashing: false,

  // 5) توجيه /api إلى خادم Django في مرحلة التطوير
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
        /offline\.html$/,
        /\/static\/data\/questions\.json$/    // ← تحميل مسبق لملف الأسئلة
      ],
      runtimeCaching: [
        {
          // API: أسئلة وكتب
          urlPattern: /^\/api\/quiz\/(?:questions|books)(?:\/|$)/,
          handler: 'NetworkFirst',
          options: {
            cacheName: 'api-cache',
            networkTimeoutSeconds: 5,
            cacheableResponse: { statuses: [0, 200] }
          }
        },
        {
          // استيراد الأسئلة أو الكتب
          urlPattern: /^\/api\/quiz\/import-(?:questions|books)(?:\/|$)/,
          handler: 'NetworkFirst',
          options: {
            cacheName: 'import-cache',
            networkTimeoutSeconds: 5,
            cacheableResponse: { statuses: [0, 200] }
          }
        },
        {
          // الموارد الثابتة (JS, CSS, صور)
          urlPattern: /\.(?:js|css|png|jpg|jpeg|svg|gif)$/,
          handler: 'CacheFirst',
          options: {
            cacheName: 'static-resources',
            cacheableResponse: { statuses: [0, 200] }
          }
        }
      ]
    }
  },

  // 7) إنشاء source maps للإنتاج لتسهيل التصحيح
  productionSourceMap: true,

  // 8) ضبط Webpack لإضافة source maps
  configureWebpack: { devtool: 'source-map' }
};
