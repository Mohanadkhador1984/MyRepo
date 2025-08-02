// src/utils/audio.js

// يحصل BASE_URL على القيمة "/" في التطوير و"/static/" في الإنتاج
const base = process.env.BASE_URL;

export const clickSound   = new Audio(`${base}quiz/sounds/click.mp3`);
export const correctSound = new Audio(`${base}quiz/sounds/correct.mp3`);
export const wrongSound   = new Audio(`${base}quiz/sounds/wrong.mp3`);

export const bgMusic = new Audio(`${base}quiz/sounds/bg-music.mp3`);
bgMusic.loop = true;
