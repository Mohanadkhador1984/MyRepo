// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import QuizPage from '@/views/QuizPage.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'QuizPage',
      component: QuizPage
    }
  ]
})
