// quiz-frontend/vue.config.js
const path = require('path')

module.exports = {
  // 1) دمج alias و devtool
  configureWebpack: {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src')
      }
    },
    // إنتاج source maps للتصحيح
    devtool: process.env.NODE_ENV === 'production' ? 'source-map' : 'eval-source-map'
  },

  // 2) إخراج البناء إلى مجلد Django frontend_dist/dist
  outputDir: path.resolve(__dirname, '..', '..', 'backend', 'frontend_dist', 'dist'),

  // 3) جميع الموارد (CSS/JS/IMG) توضع في dist/static
  assetsDir: 'static',

  // 4) publicPath يطابق STATIC_URL في Django
  publicPath: process.env.NODE_ENV === 'production' ? '/static/' : '/',

  // 5) index.html ثابت بدون هاش
  indexPath: 'index.html',
  filenameHashing: false,

  // 6) proxy لطلبات /api في طور التطوير
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

  // 7) PWA و Workbox (اختياري حسب حاجتك)
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
      include: [ /\.html$/, /\.js$/, /\.css$/, /\.png$/, /\.svg$/, /manifest\.json$/, /offline\.html$/ ],
      runtimeCaching: [
        {
          urlPattern: /^\/api\/quiz\//,
          handler: 'NetworkFirst',
          options: {
            cacheName: 'api-cache',
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

  // 8) تمكين source maps في الإنتاج
  productionSourceMap: true
}
