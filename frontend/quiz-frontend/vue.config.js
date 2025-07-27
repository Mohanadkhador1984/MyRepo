// frontend/quiz-frontend/vue.config.js

const path = require('path');

module.exports = {
  // 1) إخراج build إلى مجلد Django
  //    من quiz-frontend/dist إلى ../../backend/frontend-build/dist
  outputDir: path.resolve(__dirname, '../../backend/frontend-build/dist'),

  // 2) داخل dist، اجعل مجلد الأصول الثابتة باسم "static"
  assetsDir: 'static',

  // 3) publicPath ديناميكي: في الإنتاج يستخدم /static/vue/ وعند التطوير /
  publicPath:
    process.env.NODE_ENV === 'production'
      ? '/static/vue/'
      : '/',

  // 4) proxy لتوجيه طلبات /api أثناء التطوير إلى Django على المنفذ 8000
  devServer: {
    proxy: {
      '^/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false
      }
    }
  },

  // 5) إعدادات PWA و Workbox
  pwa: {
    workboxPluginMode: 'GenerateSW',
    workboxOptions: {
      // 5.1) اسم ملف service worker داخل dist
      swDest: 'service-worker.js',
      // 5.2) يُفعّل التحديث الفوري دون انتظار
      clientsClaim: true,
      skipWaiting: true,
      // 5.3) الأصول المراد تخزينها مسبقًا
      include: [
        /\.html$/,
        /\.js$/,
        /\.css$/,
        /\.png$/,
        /\.svg$/,
        /manifest\.json$/,
        /offline\.html$/
      ],
      // 5.4) fallback عند انقطاع الشبكة
      navigateFallback: '/offline.html',
      // 5.5) استراتيجيات التخزين الديناميكي
      runtimeCaching: [
        {
          // قراءة أسئلة وكتب الـ quiz
          urlPattern: /^\/api\/quiz\/(?:questions|books)(?:\/|$)/,
          handler: 'NetworkFirst',
          options: {
            cacheName: 'api-cache',
            networkTimeoutSeconds: 5,
            cacheableResponse: { statuses: [0, 200] }
          }
        },
        {
          // رفع الاستيراد (import)
          urlPattern: /^\/api\/quiz\/import-(?:questions|books)(?:\/|$)/,
          handler: 'NetworkFirst',
          options: {
            cacheName: 'import-cache',
            networkTimeoutSeconds: 5,
            cacheableResponse: { statuses: [0, 200] }
          }
        },
        {
          // الأصول الثابتة: JS, CSS, صور، ...
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

  // 6) إنتاج Source Maps لتسهيل التصحيح بعد النشر
  productionSourceMap: true,

  // 7) تكوين Webpack لإخراج Source Maps
  configureWebpack: {
    devtool: 'source-map'
  }
};
