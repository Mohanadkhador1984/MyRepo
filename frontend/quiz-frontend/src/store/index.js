import { createRouter, createWebHistory } from 'vue-router'
import StartScreen  from '@/views/StartScreen.vue'
import SignupScreen from '@/views/SignupScreen.vue'
import QuizPage     from '@/views/QuizPage.vue'

const routes = [
  { path:'/',       name:'Start',  component:StartScreen },
  { path:'/signup', name:'Signup', component:SignupScreen },
  { path:'/quiz',   name:'Quiz',   component:QuizPage, meta:{ requiresAuth:true } }
]

const router = createRouter({ history:createWebHistory(), routes })

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  if (to.meta.requiresAuth && !token) {
    return next({ name:'Start' })
  }
  next()
})

export default router
