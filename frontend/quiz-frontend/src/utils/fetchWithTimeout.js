// مثال على fetchWithTimeout في init()
async function init() {
  loadingQuestions.value = true
  loadError.value        = null

  const apiCall  = fetchWithTimeout(fetchQuestions(), 1500)   // مهلة 1.5 ث
  const jsonCall = loadQuestionsFromJSON()

  try {
    const data = await Promise.race([apiCall, jsonCall])
    allQ.value = Array.isArray(data) ? data : data.questions || data
  } catch {
    loadError.value = 'تعذّر تحميل الأسئلة'
  } finally {
    loadingQuestions.value = false
  }
}
