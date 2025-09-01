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

  outputDir: path.resolve(__dirname, 'dist'),
  
  
  assetsDir: '',
  publicPath: '/',



  // 4) publicPath يطابق STATIC_URL في Django
 
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
