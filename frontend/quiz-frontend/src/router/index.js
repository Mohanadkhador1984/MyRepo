import { createRouter, createWebHistory } from 'vue-router'
import StartPage from '../views/StartPage.vue'
import QuizPage from '../views/QuizPage.vue'
import DevPage from '../views/DevPage.vue'

const routes = [
  {
    path: '/',
    name: 'StartPage',
    component: StartPage,
  },
  {
    path: '/quiz',
    name: 'QuizPage',
    component: QuizPage,
    props: route => ({ activated: route.query.activated === 'true' }),
  },
  {
    path: '/dev',
    name: 'DevPage',
    component: DevPage,
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router