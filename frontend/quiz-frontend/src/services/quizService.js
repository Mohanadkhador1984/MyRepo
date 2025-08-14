// src/services/quizService.js

import { api } from '@/plugins/axios'
import questionsData from '@/assets/data/questions.json'

/**
 * جلب الأسئلة من ملف JSON محلي
 */
export async function loadQuestionsFromJSON() {
  // إذا كان JSON يحوي مصفوفة مباشرة أو كائن يحتوي مفتاح questions
  return Array.isArray(questionsData)
    ? questionsData
    : questionsData.questions || questionsData
}

/**
 * جلب الأسئلة من الـ API (باستخدام axios)
 */
export async function fetchQuestionsFromAPI() {
  const res = await api.get('quiz/questions/')
  return Array.isArray(res.data)
    ? res.data
    : res.data.questions || res.data
}

/**
 * جلب الكتب من الـ API
 */
export async function fetchBooks() {
  const res = await api.get('quiz/books/')
  if (res.status !== 200) {
    throw new Error(`فشل جلب الكتب: ${res.status}`)
  }
  return res.data
}

/**
 * استيراد الأسئلة إلى الخادم عبر API
 */
export async function importQuestions(payload) {
  const res = await api.post('quiz/import-questions/', payload)
  if (res.status !== 201 && res.status !== 200) {
    throw new Error(`فشل استيراد الأسئلة: ${res.status}`)
  }
  return res.data
}

/**
 * استيراد الكتب إلى الخادم عبر API
 */
export async function importBooks(payload) {
  const res = await api.post('quiz/import-books/', payload)
  if (res.status !== 201 && res.status !== 200) {
    throw new Error(`فشل استيراد الكتب: ${res.status}`)
  }
  return res.data
}
