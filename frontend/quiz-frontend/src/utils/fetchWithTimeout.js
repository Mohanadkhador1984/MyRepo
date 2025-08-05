export function fetchWithTimeout(promise, ms = 3000) {
  const timeout = new Promise((_, reject) =>
    setTimeout(() => reject(new Error('Timeout')), ms)
  );
  return Promise.race([promise, timeout]);
}
