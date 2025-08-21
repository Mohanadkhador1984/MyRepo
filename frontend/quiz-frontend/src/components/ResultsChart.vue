<template>
  <div class="results-container luxury">

    <!-- العنوان الفخم -->
    <h2 class="title">نتائج الاختبار</h2>

    <!-- حقول الإدخال -->
    <div class="inputs-wrapper">
      <div class="input-group">
        <input
          id="studentName"
          v-model="studentName"
          type="text"
          placeholder=" "
          required
        />
        <label for="studentName">اسم الطالب</label>
      </div>

      <div class="input-group">
        <input
          id="teacherPhone"
          v-model="teacherPhone"
          type="tel"
          placeholder=" "
          required
        />
        <label for="teacherPhone">رقم جوال المدرس</label>
        <small class="hint">مثال: 0953447860 — يبدأ بـ09 ويحتوي 10 أرقام</small>
      </div>

      <!-- زر واتساب يظهر أسفل حقل رقم المدرس -->
      <button
        class="btn send"
        :disabled="!canSend"
        @click="sendReport"
      >
        <i class="fab fa-whatsapp"></i>
        إرسال النتائج عبر واتساب
      </button>
    </div>

    <!-- بطاقات الملخص -->
    <div class="cards-grid">
      <div class="card correct">
        <i class="fas fa-check-circle"></i>
        <div class="text">
          <span class="num">{{ correct }}</span>
          <span class="desc">صحيحة</span>
        </div>
      </div>
      <div class="card wrong">
        <i class="fas fa-times-circle"></i>
        <div class="text">
          <span class="num">{{ wrong }}</span>
          <span class="desc">خاطئة</span>
        </div>
      </div>
      <div class="card total">
        <i class="fas fa-list-ol"></i>
        <div class="text">
          <span class="num">{{ total }}</span>
          <span class="desc">الإجمالي</span>
        </div>
      </div>
      <div class="card percent">
        <i class="fas fa-percentage"></i>
        <div class="text">
          <span class="num">{{ percentage }}%</span>
          <span class="desc">نسبة النجاح</span>
        </div>
      </div>
    </div>

    <!-- الرسم الدائري -->
    <div class="chart-box">
      <canvas ref="doughnutCanvas"></canvas>
    </div>

    <!-- زر إعادة الاختبار -->
    <button class="btn reset" @click="$emit('reset')">
      إعادة الاختبار
    </button>
  </div>
</template>

<script setup>
/* eslint-disable no-undef */
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import Chart from 'chart.js/auto'

// نعرف props باستخدام defineProps
const props = defineProps({
  correct:    { type: Number, required: true },
  wrong:      { type: Number, required: true },
  percentage: { type: Number, required: true }
})

const studentName    = ref('')
const teacherPhone   = ref('')
const doughnutCanvas = ref(null)
let   chartInstance  = null

// حسابات التلخيص والصلاحية
const total     = computed(() => props.correct + props.wrong)
const nameValid = computed(() => studentName.value.trim().length > 0)
const phoneValid= computed(() => /^09[0-9]{8}$/.test(teacherPhone.value.trim()))
const canSend   = computed(() => nameValid.value && phoneValid.value)

// دالة رسم المخطط الدائري
function renderChart() {
  if (!doughnutCanvas.value) return

  // تدمير أي مخطط سابق
  if (chartInstance) {
    chartInstance.destroy()
  }

  chartInstance = new Chart(doughnutCanvas.value, {
    type: 'doughnut',
    data: {
      labels: ['صحيحة', 'خاطئة'],
      datasets: [{
        data: [props.correct, props.wrong],
        backgroundColor: ['#FFD700', '#FF4C4C'],
        hoverBackgroundColor: ['#FFC200', '#E60000'],
        borderWidth: 0
      }]
    },
    options: {
      cutout: '75%',
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label(ctx) {
              const cnt = ctx.parsed
              const pct = Math.round((cnt / total.value) * 100)
              return `${ctx.label}: ${cnt} (${pct}%)`
            }
          }
        }
      }
    }
  })
}

// دالة إرسال التقرير عبر واتساب
function sendReport() {
  if (!canSend.value) return

  const msg = encodeURIComponent(
    `📋 نتائج الاختبار\n` +
    `👤 الطالب: ${studentName.value}\n` +
    `✅ صحيحة: ${props.correct}\n` +
    `❌ خاطئة: ${props.wrong}\n` +
    `📊 نسبة: ${props.percentage}%\n` +
    `🔢 الإجمالي: ${total.value}`
  )

  window.open(
    `https://api.whatsapp.com/send?phone=${teacherPhone.value}&text=${msg}`,
    '_blank'
  )
}

// ربط دورة الحياة
onMounted(renderChart)
watch([() => props.correct, () => props.wrong], renderChart)
onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.destroy()
    chartInstance = null
  }
})
</script>

<style scoped>
/* استيراد الخطوط والرموز */
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css');

.results-container {
  max-width: 640px;
  margin: 2.5rem auto;
  padding:4.5rem;
  border-radius: 24px;
  background: rgba(255,255,255,0.1);
  backdrop-filter: blur(20px);
  box-shadow: 0 16px 40px rgba(0,0,0,0.5);
  color: #fff;
  position: relative;
  font-family: 'Cairo', sans-serif;
}

.results-container.luxury {
  border: 3px solid transparent;
  border-image: linear-gradient(45deg, #FFD700, #FFC107, #FFD700) 1;
}

.title {
  font-size: 2.8rem;
  font-weight: 800;
  text-align: center;
  margin-bottom: 2rem;
  background: linear-gradient(90deg, #FFD700, #FFC107);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.inputs-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 2rem;
}
.input-group {
  position: relative;
}
.input-group input {
  width: 100%;
  padding: 1rem 1.2rem;
  border: 2px solid rgba(255,255,255,0.3);
  border-radius: 12px;
  background: rgba(255,255,255,0.05);
  color: #fff;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s, box-shadow 0.3s;
}
.input-group input:focus {
  border-color: #FFD700;
  box-shadow: 0 0 12px rgba(255,215,0,0.6);
}
.input-group label {
  position: absolute;
  top: -0.7rem;
  left: 1rem;
  background: rgba(0,0,0,0.5);
  padding: 0 0.4rem;
  font-size: 0.85rem;
  color: #FFD700;
}

.btn.send {
  display: block;
  margin: 1rem auto 2rem;
  padding: 0.9rem 2rem;
  font-size: 1rem;
  font-weight: 700;
  background: linear-gradient(90deg, #25D366, #128C7E);
  border: none;
  border-radius: 50px;
  color: #fff;
  cursor: pointer;
  transition: background 0.3s, transform 0.1s, opacity 0.3s;
  opacity: 1;
}
.btn.send:disabled {
  background: rgba(255,255,255,0.2);
  color: rgba(255,255,255,0.6);
  cursor: not-allowed;
  opacity: 0.7;
}
.btn.send:not(:disabled):hover {
  background: linear-gradient(90deg, #128C7E, #25D366);
  transform: translateY(-2px);
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}
.card {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 1.2rem;
  border-radius: 12px;
  background: rgba(0,0,0,0.3);
  box-shadow: 0 6px 20px rgba(0,0,0,0.5);
  transition: transform 0.2s;
}
.card:hover { transform: translateY(-4px); }
.card.correct  { border-left: 4px solid #00C851; }
.card.wrong    { border-left: 4px solid #CC0000; }
.card.total    { border-left: 4px solid #33b5e5; }
.card.percent  { border-left: 4px solid #ffbb33; }
.card i {
  font-size: 1.6rem;
  color: #FFD700;
}
.card .num {
  font-size: 1.4rem;
  font-weight: 700;
}
.card .desc {
  font-size: 0.85rem;
  opacity: 0.8;
}

.chart-box {
  width: 100%;
  max-width: 280px;
  height: 280px;
  margin: 0 auto 2rem;
}

.btn.reset {
  display: block;
  width: 100%;
  padding: 0.9rem;
  font-size: 1rem;
  font-weight: 600;
  background: rgba(255,255,255,0.1);
  border: 2px solid rgba(255,255,255,0.3);
  border-radius: 12px;
  color: #fff;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
}
.btn.reset:hover {
  background: rgba(255,255,255,0.2);
  transform: translateY(-2px);
}


</style>
