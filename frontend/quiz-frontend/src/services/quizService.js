// src/services/quizService.js

/**
 * جلب الأسئلة من قاعدة البيانات عبر API
 */
// src/services/quizService.js

// 1) استيراد JSON مضمّن داخل Bundle
import questionsData from '@/assets/data/questions.json';

// 2) دالة لإرجاع الأسئلة من JSON
export async function loadQuestionsFromJSON() {
  return questionsData;
}

// 3) دالة اتصال API (اختياري)
export async function fetchQuestionsFromAPI() {
  const response = await fetch('/api/quiz/questions/');
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  const data = await response.json();
  return Array.isArray(data) ? data : data.questions || data;
}





/**
 * جلب الكتب من قاعدة البيانات عبر API
 */
export async function fetchBooks() {
  const res = await fetch('/api/quiz/books/');
  if (!res.ok) {
    throw new Error(`فشل جلب الكتب: ${res.status}`);
  }
  return await res.json();
}

// إذا كنت تحتاج نقطتي الاستيراد أوفلاين:
export async function importQuestions(payload) {
  const res = await fetch('/api/quiz/import-questions/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    throw new Error(`فشل استيراد الأسئلة: ${res.status}`);
  }
  return await res.json();
}

export async function importBooks(payload) {
  const res = await fetch('/api/quiz/import-books/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    throw new Error(`فشل استيراد الكتب: ${res.status}`);
  }
  return await res.json();
}
