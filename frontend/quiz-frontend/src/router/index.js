// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

// استيراد المكونات حسب مكان وجودها
import StartScreen   from '@/components/StartScreen.vue'
import SignupScreen  from '@/components/SignupScreen.vue'
import LoginScreen   from '@/views/LoginScreen.vue'
import QuizPage      from '@/views/QuizPage.vue'

const routes = [
  {
    path: '/',
    name: 'Start',
    component: StartScreen
  },
  {
    path: '/signup',
    name: 'Signup',
    component: SignupScreen
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginScreen
  },
  {
    path: '/quiz',
    name: 'Quiz',
    component: QuizPage,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// حماية المسارات التي تتطلب تسجيل دخول
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')

  // الصفحات التي لا تحتاج مصادقة
  if (['Start', 'Login', 'Signup'].includes(to.name)) {
    return next()
  }

  // إذا لم يوجد توكن انتقل إلى صفحة البداية
  if (!token) {
    return next({ name: 'Start' })
  }

  // خلاف ذلك، تابع الانتقال
  next()
})

export default router
