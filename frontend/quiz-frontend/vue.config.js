// vue.config.js
const path = require('path')

module.exports = {
  publicPath: process.env.NODE_ENV === 'production' ? '/static/' : '/',
  outputDir: path.resolve(__dirname, '..','backend','frontend_dist','dist'),
  assetsDir: 'static',
  indexPath: 'index.html',
  filenameHashing: false,
  productionSourceMap: true,

  configureWebpack: {
    resolve: { alias: { '@': path.resolve(__dirname,'src') } },
    devtool: process.env.NODE_ENV === 'production'
      ? 'source-map'
      : 'eval-source-map'
  },

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

  pwa: {
    workboxPluginMode: 'InjectManifest',
    workboxOptions: {
      swSrc: path.resolve(__dirname,'src','service-worker.js'),
      swDest: 'service-worker.js'
    }
  }
}
