// src/utils/fetchWithTimeout.js
export async function fetchWithTimeout(fetchPromise, timeout = 3000) {
  let timeoutHandle;
  const timeoutPromise = new Promise((_, reject) => {
    timeoutHandle = setTimeout(() => {
      reject(new Error('Timeout exceeded'));
    }, timeout);
  });

  return Promise.race([
    fetchPromise,
    timeoutPromise
  ]).finally(() => clearTimeout(timeoutHandle));
}