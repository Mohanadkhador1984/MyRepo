// src/services/quizService.js

/**
 * جلب الأسئلة من قاعدة البيانات عبر API
 */
// src/services/quizService.js
export async function fetchQuestions() {
  const res = await fetch('/api/quiz/questions/');
  console.log('Fetch /api/quiz/questions/ status:', res.status);
  const text = await res.text();
  console.log('Fetch response text:', text);
  if (!res.ok) {
    throw new Error(`فشل جلب الأسئلة: ${res.status}`);
  }
  const data = JSON.parse(text);
  console.log('Parsed JSON data:', data);
  return data;
}


// تحميل JSON ثابت
export async function loadQuestionsFromJSON() {
  const res = await fetch('/static/data/questions.json');
  if (!res.ok) throw new Error('JSON load failed');
  return res.json();
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
