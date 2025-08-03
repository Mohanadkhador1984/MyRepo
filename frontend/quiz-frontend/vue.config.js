// frontend/quiz-frontend/vue.config.js

const path = require('path');

module.exports = {
  outputDir: path.resolve(__dirname, '..', '..', 'backend', 'frontend_dist', 'dist'),

  assetsDir: 'static', // ← ينقل كل CSS/JS/IMG إلى dist/static

  publicPath: process.env.NODE_ENV === 'production'
    ? '/static/' // ← مهم جداً: يجعل الروابط تبدأ بـ /static/ في الإنتاج
    : '/',
    
  indexPath: 'index.html', // ← أي اسم آخر يسبب مشاكل في Django
  filenameHashing: false, // ← يساعد في التعرف على الملفات بسهولة

  // 5) إعداد خادم التطوير وتوجيه /api إلى Django
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

  // 6) إعداد PWA
  pwa: {
    name: 'Quiz App',
    themeColor: '#42b983',
    msTileColor: '#000000',
    workboxPluginMode: 'GenerateSW',
    workboxOptions: {
      swDest: 'service-worker.js',
      clientsClaim: true,
      skipWaiting: true,
      include: [
        /\.html$/,
        /\.js$/,
        /\.css$/,
        /\.png$/,
        /\.svg$/,
        /manifest\.json$/,
        /offline\.html$/
      ],
      navigateFallback: '/offline.html',
      runtimeCaching: [
        {
          urlPattern: /^\/api\/quiz\/(?:questions|books)(?:\/|$)/,
          handler: 'NetworkFirst',
          options: {
            cacheName: 'api-cache',
            networkTimeoutSeconds: 5,
            cacheableResponse: { statuses: [0, 200] }
          }
        },
        {
          urlPattern: /^\/api\/quiz\/import-(?:questions|books)(?:\/|$)/,
          handler: 'NetworkFirst',
          options: {
            cacheName: 'import-cache',
            networkTimeoutSeconds: 5,
            cacheableResponse: { statuses: [0, 200] }
          }
        },
        {
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

  // 7) إنشاء خرائط Source Maps للإنتاج للتسهيل عند التصحيح
  productionSourceMap: true,

  // 8) ضبط Webpack لإنتاج Source Maps
  configureWebpack: {
    devtool: 'source-map'
  }
};
