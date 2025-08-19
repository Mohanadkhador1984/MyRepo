// src/utils/audio.js
const base = process.env.BASE_URL;  // "/" أو "/static/" حسب بيئتك

// إنشاء AudioContext موحد
const audioContext = new (window.AudioContext || window.webkitAudioContext)();
const bufferCache = {};

// دالة لتحميل وفك ترميز الصوت وتخزينه في الذاكرة
async function loadBuffer(path) {
  if (bufferCache[path]) {
    return bufferCache[path];
  }

  const response = await fetch(`${base}quiz/sounds/${path}`);
  const arrayBuffer = await response.arrayBuffer();
  const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
  bufferCache[path] = audioBuffer;
  return audioBuffer;
}

// دالة تشغيل الصوت مع خيار التكرار
export async function playSound(path, { loop = false } = {}) {
  // استئناف السياق لو كان متوقفاً (بعض المتصفحات تتطلب تفاعل مستخدم)
  if (audioContext.state === 'suspended') {
    await audioContext.resume();
  }

  const buffer = await loadBuffer(path);
  const source = audioContext.createBufferSource();
  source.buffer = buffer;
  source.loop = loop;
  source.connect(audioContext.destination);
  source.start(0);
  return source;
}

// ربط الاختصارات
export const playClick   = () => playSound('click.mp3');
export const playCorrect = () => playSound('correct.mp3');
export const playWrong   = () => playSound('wrong.mp3');
export const playBgMusic = () => playSound('bg-music.mp3', { loop: true });
