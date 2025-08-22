// src/utils/audio.js
const base = process.env.BASE_URL; // "/" أو "/static/" حسب البيئة

const makeAudio = (path) => {
  const audio = new Audio(`${base}quiz/sounds/${path}`);
  audio.load();
  return audio;
};

export const clickSound   = makeAudio('click.mp3');
export const correctSound = makeAudio('correct.mp3');
export const wrongSound   = makeAudio('discorrect.mp3');
export const bgMusic      = makeAudio('bg-music.mp3');
bgMusic.loop = true;
