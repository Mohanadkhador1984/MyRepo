// project-root/vue.config.js
const { defineConfig } = require('@vue/cli-service')
const path = require('path')

module.exports = defineConfig({
  // 1) المسار العام: /static/ في الإنتاج، / في التطوير
  publicPath: process.env.NODE_ENV === 'production'
    ? '/static/'
    : '/',

  // 2) مجلد الخرج ليتوافق مع Django
  outputDir: path.resolve(__dirname, 'backend', 'frontend_dist', 'dist'),

  // 3) مجلد الأصول الثابتة داخل dist
  assetsDir: 'static',

  // 4) index.html ثابت بدون هاش
  indexPath: 'index.html',
  filenameHashing: false,

  // 5) احتفظ بالـ source maps حتى في الإنتاج للتصحيح
  productionSourceMap: true,

  // 6) إعدادات Webpack العامة
  configureWebpack: {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src')
      }
    },
    // اختيار نوع الـ devtool لكل بيئة
    devtool: process.env.NODE_ENV === 'production'
      ? 'source-map'
      : 'eval-source-map'
  },

  // 7) تعديل سلسلة Webpack (chainWebpack) لتحسين Prefetch/Preload
  chainWebpack: config => {
    // احذف prefetch الافتراضي إن لم تكن بحاجة له
    config.plugins.delete('prefetch')

    // فعّل preload لجميع الشظايا
    config.plugin('preload').tap(options => {
      options[0].include = 'allChunks'
      return options
    })
  },

  // 8) proxy لطلبات API في طور التطوير
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

  // 9) إعداد PWA مع InjectManifest لاستخدام service-worker.js المخصص
  pwa: {
    name: 'Quiz App',
    themeColor: '#42b983',
    msTileColor: '#000000',
    appleMobileWebAppCapable: 'yes',
    appleMobileWebAppStatusBarStyle: 'black',

    workboxPluginMode: 'InjectManifest',
    workboxOptions: {
      // مسار ملف الـ SW المخصص داخل src/
      swSrc: path.resolve(__dirname, 'src', 'service-worker.js'),
      // اسم الملف النهائي ضمن dist/
      swDest: 'service-worker.js',
      // استثناء ملفات خارجة عن الحاجة
      exclude: [ /\.map$/, /manifest\.json$/ ]
    }
  }
})
