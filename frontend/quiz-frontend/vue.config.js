// frontend/quiz-frontend/vue.config.js

const path = require('path');

module.exports = {
  // 1) إخراج build إلى مجلد Django
   // Drop all build output into your Django static directory
  outputDir: path.resolve(__dirname, '../../backend/frontend_dist'),
  // Inside that folder, put JS/CSS under "static" (or whatever you configured)
  assetsDir: 'static',
  // Set publicPath so asset URLs match Django’s STATIC_URL
  // If your Django STATIC_URL = '/static/', then:
  publicPath: '/static/',

  // 4) proxy لتوجيه طلبات /api أثناء التطوير إلى Django على المنفذ 8000
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

  // 5) إعدادات PWA
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
            cacheableResponse: {
              statuses: [0, 200]
            }
          }
        },
        {
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

  // 6) إنتاج source maps لتسهيل التصحيح بعد النشر
  productionSourceMap: true,

  // 7) إعداد Webpack لتوليد source maps
  configureWebpack: {
    devtool: 'source-map'
  }
};