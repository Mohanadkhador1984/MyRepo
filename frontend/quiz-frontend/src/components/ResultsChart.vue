<!-- src/components/ResultsChart.vue -->
<template>
  <div class="results-container ultra-lux">

    <!-- العنوان -->
    <h2 class="title shimmer">نتائج الاختبار</h2>

    <!-- حقول الإدخال -->
    <div class="inputs-wrapper">
      <div class="input-group slide-in-left" style="--delay: 0.1s">
        <input
          id="studentName"
          v-model="studentName"
          type="text"
          placeholder=" "
          autocomplete="off"
        />
        <label for="studentName">اسم الطالب</label>
      </div>

      <div class="input-group slide-in-left" style="--delay: 0.2s">
        <input
          id="teacherPhone"
          v-model="teacherPhone"
          type="tel"
          placeholder=" "
          autocomplete="off"
        />
        <label for="teacherPhone">رقم جوال المدرس</label>
        <small class="hint">مثال: 0953447860 — يبدأ بـ09 ويحتوي 10 أرقام</small>
      </div>

      <!-- زر واتساب -->
      <button
        class="btn send pop-in"
        :class="{ active: canSend }"
        :disabled="!canSend"
        @click="sendReport"
        style="--delay: 0.3s"
      >
        <i class="fab fa-whatsapp fa-lg"></i>
        إرسال عبر واتساب
      </button>
    </div>

    <!-- بطاقات الملخص -->
    <div class="cards-grid">
      <div
        v-for="(card, idx) in cardData"
        :key="idx"
        class="card pop-in"
        :class="card.type"
        :style="{ '--delay': (0.2 + idx * 0.1) + 's' }"
      >
        <i :class="card.icon"></i>
        <div class="text">
          <span class="num">{{ card.value }}</span>
          <span class="desc">{{ card.label }}</span>
        </div>
      </div>
    </div>

    <!-- الرسم الدائري -->
    <div class="chart-box fade-in" :class="{ visible: chartReady }" style="--delay: 0.6s">
      <canvas ref="doughnutCanvas"></canvas>
    </div>

    <!-- زر إعادة الاختبار -->
    <button class="btn reset pop-in" @click="$emit('reset')" style="--delay: 0.7s">
      إعادة الاختبار
    </button>
  </div>
</template>

<script setup>
/* eslint-disable no-undef */
import { ref, computed, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import Chart from 'chart.js/auto'

// تعريف الخصائص
const props = defineProps({
  correct:    { type: Number, required: true },
  wrong:      { type: Number, required: true },
  percentage: { type: Number, required: true }
})

// Reactive state
const studentName    = ref('')
const teacherPhone   = ref('')
const doughnutCanvas = ref(null)
const chartReady     = ref(false)
let chartInstance    = null

// Computed
const total     = computed(() => props.correct + props.wrong)
const nameValid = computed(() => studentName.value.trim().length > 0)
const phoneValid= computed(() => /^09[0-9]{8}$/.test(teacherPhone.value.trim()))
const canSend   = computed(() => nameValid.value && phoneValid.value)

// مجموعة بيانات البطاقات
const cardData = computed(() => [
  { label: 'صحيحة', value: props.correct, icon: 'fas fa-check-circle', type: 'correct' },
  { label: 'خاطئة', value: props.wrong,   icon: 'fas fa-times-circle',   type: 'wrong' },
  { label: 'الإجمالي', value: total.value, icon: 'fas fa-list-ol',       type: 'total' },
  { label: 'نسبة النجاح', value: props.percentage + '%', icon: 'fas fa-percentage', type: 'percent' },
])

// رسم المخطط
function renderChart() {
  if (!doughnutCanvas.value) return
  if (chartInstance) chartInstance.destroy()

  chartInstance = new Chart(doughnutCanvas.value, {
    type: 'doughnut',
    data: {
      labels: ['صحيحة', 'خاطئة'],
      datasets: [{
        data: [props.correct, props.wrong],
        backgroundColor: ['#16a34a', '#dc2626'],
        hoverBackgroundColor: ['#15803d', '#b91c1c'],
        borderWidth: 2,
        borderColor: '#111'
      }]
    },
    options: {
      cutout: '70%',
      animation: {
        animateRotate: true,
        duration: 1000
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#333',
          titleColor: '#fff',
          bodyColor: '#fff',
          borderColor: '#16a34a',
          borderWidth: 1,
          callbacks: {
            label(ctx) {
              const cnt = ctx.parsed
              const pct = Math.round((cnt / total.value) * 100)
              return ` ${ctx.label}: ${cnt} (${pct}%) `
            }
          }
        }
      }
    }
  })

  // تأخير بسيط قبل إظهار العنصر
  chartReady.value = false
  setTimeout(() => (chartReady.value = true), 200)
}

// إرسال التقرير عبر واتساب
function sendReport() {
  if (!canSend.value) return
  const msg = encodeURIComponent(
    `🎓 نتائج الاختبار 🎓\n\n` +
    `👤 الطالب: ${studentName.value}\n` +
    `✅ صحيحة: ${props.correct}\n` +
    `❌ خاطئة: ${props.wrong}\n` +
    `📊 نسبة النجاح: ${props.percentage}%\n` +
    `📋 الإجمالي: ${total.value}`
  )
  window.open(`https://api.whatsapp.com/send?phone=${teacherPhone.value}&text=${msg}`, '_blank')
}

// دورة الحياة
onMounted(async () => {
  await nextTick()
  renderChart()
})
watch([() => props.correct, () => props.wrong], () => nextTick(renderChart))
onBeforeUnmount(() => {
  if (chartInstance) chartInstance.destroy()
})
</script>

<style scoped>
/* استيراد الخطوط والأيقونات */
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css');

/* متغيرات الألوان */
:root {
  --primary: #16a34a;
  --primary-dark: #15803d;
  --danger: #dc2626;
  --danger-dark: #b91c1c;
  --glass-bg: rgba(255,255,255,0.1);
  --glass-blur: blur(20px);
  --text-light: #f7f7f7;
  --golden: #fbbf24;
}

/* الحاوية الرئيسية */
.results-container.ultra-lux {
  font-family: 'Cairo', sans-serif;
  max-width: 680px;
  margin: 3rem auto;
  padding: 2.5rem;
  border-radius: 24px;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  box-shadow: 0 8px 32px rgba(0,0,0,0.7);
  border: 2px solid rgba(255,255,255,0.3);
  position: relative;
  overflow: hidden;
  color: var(--text-light);
}

/* تأثير الانعكاس المتحرّك */
.results-container.ultra-lux::after {
  content: '';
  position: absolute;
  top: -50%; left: -50%;
  width: 200%; height: 200%;
  background: radial-gradient(circle at center, rgba(255,255,255,0.3), transparent 70%);
  animation: rotate 8s linear infinite;
}
@keyframes rotate {
  to { transform: rotate(360deg); }
}

/* العنوان */
.title {
  font-size: 2.8rem;
  font-weight: 800;
  text-align: center;
  margin-bottom: 2rem;
  color: var(--golden);
  text-shadow: 0 0 8px rgba(255,191,36,0.8);
  opacity: 0;
  animation: fadeIn 1s forwards;
}
.shimmer {
  background: linear-gradient(90deg, var(--golden), #fff, var(--golden));
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
  animation: shimmer 2s infinite;
}

/* Inputs */
.inputs-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  margin-bottom: 2rem;
}
.input-group {
  position: relative;
  opacity: 0;
  transform: translateX(-20px);
  animation: slideIn 0.6s forwards;
  animation-delay: var(--delay);
}
.input-group input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid rgba(255,255,255,0.3);
  border-radius: 12px;
  background: rgba(0,0,0,0.4);
  color: var(--text-light);
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s, box-shadow 0.3s;
}
.input-group input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 8px var(--primary);
}
.input-group label {
  position: absolute;
  top: -0.6rem; left: 1rem;
  background: var(--glass-bg);
  padding: 0 0.4rem;
  font-size: 0.85rem;
  color: var(--primary);
  font-weight: 600;
}
.hint {
  display: block;
  margin-top: 0.3rem;
  font-size: 0.75rem;
  color: var(--primary-dark);
}

/* زر الواتساب */
.btn.send {
  display: block;
  width: 100%;
  padding: 0.75rem;
  margin: 1rem 0 2rem;
  font-size: 1rem;
  font-weight: 700;
  color: #111;
  background: var(--primary);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.5);
  border: 2px solid var(--primary-dark);
  cursor: pointer;
  opacity: 0;
  transform: translateY(20px);
  animation: popIn 0.5s forwards;
  animation-delay: var(--delay);
}
.btn.send:disabled {
  background: rgba(255,255,255,0.3);
  color: rgba(255,255,255,0.6);
  cursor: not-allowed;
}
.btn.send:not(:disabled):hover {
  background: var(--primary-dark);
}

/* بطاقات الملخص */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}
.card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  border-radius: 12px;
  background: rgba(0,0,0,0.4);
  box-shadow: inset 0 0 8px rgba(0,0,0,0.5), 0 2px 8px rgba(0,0,0,0.7);
  color: var(--text-light);
  opacity: 0;
  transform: translateY(20px);
  animation: popIn 0.5s forwards;
  animation-delay: var(--delay);
}
.card.correct { border-left: 4px solid var(--primary); }
.card.wrong   { border-left: 4px solid var(--danger); }
.card.total   { border-left: 4px solid #3b82f6; }
.card.percent { border-left: 4px solid #f59e0b; }
.card i {
  font-size: 1.5rem;
  color: var(--golden);
}
.card .num {
  font-size: 1.3rem;
  font-weight: 700;
}
.card .desc {
  font-size: 0.85rem;
  opacity: 0.9;
}

/* الرسم الدائري */
.chart-box {
  width: 100%;
  max-width: 260px;
  height: 260px;
  margin: 0 auto 2rem;
  border-radius: 50%;
  background: rgba(255,255,255,0.05);
  box-shadow: inset 0 0 12px rgba(0,0,0,0.5);
  opacity: 0;
  transform: scale(0.8);
  animation: fadeInScale 0.6s forwards;
  animation-delay: var(--delay);
}
.chart-box.visible {
  animation-delay: 0.6s;
}

/* زر إعادة الاختبار */
.btn.reset {
  display: block;
  width: 100%;
  padding: 0.75rem;
  margin-top: 1rem;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-light);
  background: transparent;
  border: 2px solid rgba(255,255,255,0.3);
  border-radius: 12px;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
  opacity: 0;
  transform: translateY(20px);
  animation: popIn 0.5s forwards;
  animation-delay: 0.8s;
}
.btn.reset:hover {
  background: rgba(255,255,255,0.1);
}

/* Keyframes */
@keyframes fadeIn {
  to { opacity: 1; }
}
@keyframes shimmer {
  0% { background-position: -200px 0; }
  100% { background-position: 200px 0; }
}
@keyframes slideIn {
  to { opacity: 1; transform: translateX(0); }
}
@keyframes popIn {
  to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInScale {
  to { opacity: 1; transform: scale(1); }
}
</style>
