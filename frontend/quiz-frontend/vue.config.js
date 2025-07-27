// frontend/quiz-frontend/vue.config.js

const path = require('path');

module.exports = {
  // 1) إخراج build في مجلد Django
  outputDir: path.resolve(__dirname, '../backend/frontend_build/dist'),
  
  // 2) مجلد الأصول داخل `dist`
  assetsDir: 'static',

  // 3) publicPath ديناميكي حسب البيئة
  publicPath:
    process.env.NODE_ENV === 'production'
      ? '/static/vue/'   // مسار الإنتاج
      : '/',              // مسار التطوير

  // 4) proxy لتوجيه طلبات الـ API خلال التطوير
  devServer: {
    proxy: {
      '^/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
};


  // 4) إعدادات PWA و Workbox
  pwa: {
    workboxPluginMode: 'GenerateSW',
    workboxOptions: {
      // 4.1) اسم ملف الـ Service Worker في مجلد dist
      swDest: 'service-worker.js',

      // 4.2) تحديث فوري دون انتظار المستخدم
      clientsClaim: true,
      skipWaiting: true,

      // 4.3) الأصول التي نرغب بتخزينها مسبقاً
      include: [
        /\.html$/,
        /\.js$/,
        /\.css$/,
        /\.png$/,
        /\.svg$/,
        /manifest\.json$/,
        /offline\.html$/
      ],

      // 4.4) صفحة fallback عند التنقل أوفلاين
      navigateFallback: '/offline.html',

      // 4.5) استراتيجيات التخزين الديناميكي
      runtimeCaching: [
        {
          // API للقراءة (questions & books)
          urlPattern: /^\/api\/quiz\/(?:questions|books)(?:\/|$)/,
          handler: 'NetworkFirst',
          options: {
            cacheName: 'api-cache',
            networkTimeoutSeconds: 5,
            cacheableResponse: { statuses: [0, 200] }
          }
        },
        {
          // API للرفع (import)
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

  // 5) source maps للإنتاج لتسهيل تصحيح الأخطاء
  productionSourceMap: true,
  configureWebpack: {
    devtool: 'source-map'
  }
};
