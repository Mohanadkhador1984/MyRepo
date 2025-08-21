<!-- src/components/ResultsChart.vue -->
<template>
  <div class="results-container">

    <!-- العنوان -->
    <h2 class="title">نتائج الاختبار</h2>

    <!-- حقول الإدخال -->
    <div class="inputs-wrapper">
      <div class="input-group">
        <input
          id="studentName"
          v-model="studentName"
          type="text"
          required
        />
        <label for="studentName">اسم الطالب</label>
      </div>

      <div class="input-group">
        <input
          id="teacherPhone"
          v-model="teacherPhone"
          type="tel"
          required
          pattern="^[0-9]{11}$"
        />
        <label for="teacherPhone">رقم جوال المدرس (مثال: 09999111111)</label>
      </div>
    </div>

    <!-- بطاقات الملخص -->
    <div class="cards-grid">
      <div class="card correct">
        <i class="fas fa-check-circle"></i>
        <div class="text">
          <span class="number">{{ correct }}</span>
          <span class="desc">صحيحة</span>
        </div>
      </div>
      <div class="card wrong">
        <i class="fas fa-times-circle"></i>
        <div class="text">
          <span class="number">{{ wrong }}</span>
          <span class="desc">خاطئة</span>
        </div>
      </div>
      <div class="card total">
        <i class="fas fa-list-ol"></i>
        <div class="text">
          <span class="number">{{ total }}</span>
          <span class="desc">الإجمالي</span>
        </div>
      </div>
      <div class="card percent">
        <i class="fas fa-percentage"></i>
        <div class="text">
          <span class="number">{{ percentage }}%</span>
          <span class="desc">نسبة النجاح</span>
        </div>
      </div>
    </div>

    <!-- الرسم الدائري -->
    <div class="chart-box">
      <canvas ref="doughnutCanvas"></canvas>
    </div>

    <!-- زر إرسال الواتساب -->
    <button
      ref="sendBtn"
      v-if="studentNameValid && teacherPhoneValid"
      class="btn send"
      @click="sendReport"
    >
      إرسال النتائج عبر واتساب
    </button>

    <!-- زر إعادة الاختبار -->
    <button class="btn reset" @click="$emit('reset')">
      إعادة الاختبار
    </button>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import Chart from 'chart.js/auto'

export default {
  name: 'ResultsChart',
  props: {
    correct:    { type: Number, required: true },
    wrong:      { type: Number, required: true },
    percentage: { type: Number, required: true }
  },
  setup(props) {
    const studentName  = ref('')
    const teacherPhone = ref('')
    const sendBtn      = ref(null)
    const total        = computed(() => props.correct + props.wrong)

    // صلاحية الحقول
    const studentNameValid  = computed(() => studentName.value.trim().length > 0)
    const teacherPhoneValid = computed(() => /^[0-9]{11}$/.test(teacherPhone.value.trim()))

    // تمرير العرض إلى زر الإرسال عند تفعيل الحقلين
    watch(
      [studentNameValid, teacherPhoneValid],
      ([nameOk, phoneOk]) => {
        if (nameOk && phoneOk) {
          nextTick(() => {
            sendBtn.value?.scrollIntoView({ behavior: 'smooth', block: 'center' })
          })
        }
      }
    )

    // رسم المخطط الدائري
    const doughnutCanvas = ref(null)
    const renderChart = () => {
      if (!doughnutCanvas.value) return
      new Chart(doughnutCanvas.value, {
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
                  const v = ctx.parsed
                  const p = Math.round((v / total.value) * 100)
                  return `${ctx.label}: ${v} (${p}%)`
                }
              }
            }
          }
        }
      })
    }

    // إرسال التقرير عبر واتساب
    const sendReport = () => {
      const text = encodeURIComponent(
        `📋 نتائج الاختبار\n\n` +
        `👤 الطالب: ${studentName.value}\n` +
        `✅ صحيحة: ${props.correct}\n` +
        `❌ خاطئة: ${props.wrong}\n` +
        `📊 نسبة: ${props.percentage}%\n` +
        `🔢 الإجمالي: ${total.value}`
      )
      window.open(`https://api.whatsapp.com/send?phone=${teacherPhone.value}&text=${text}`, '_blank')
    }

    onMounted(renderChart)
    watch([() => props.correct, () => props.wrong], renderChart)

    return {
      studentName, teacherPhone, sendBtn,
      studentNameValid, teacherPhoneValid,
      doughnutCanvas, total,
      sendReport
    }
  }
}
</script>

<style scoped>
/* خطوط وأيقونات */
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css');

.results-container {
  max-width: 700px;
  margin: 3rem auto;
  padding: 2rem 3.5rem;
  border-radius: 16px;
  background: rgba(20, 20, 30, 0.6);
  backdrop-filter: blur(15px);
  color: #eee;
  box-shadow: 0 8px 24px rgba(0,0,0,0.6);
}

/* العنوان */
.title {
  font-family: 'Cairo', sans-serif;
  font-size: 2.4rem;
  font-weight: 800;
  text-align: center;
  margin-bottom: 1.5rem;
  background: linear-gradient(90deg, #FFD700, #FFA500);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Inputs */
.inputs-wrapper {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  margin-bottom: 2rem;
}

.input-group {
  position: relative;
  font-family: 'Cairo', sans-serif;
}

.input-group input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #444;
  border-radius: 8px;
  background: rgba(255,255,255,0.05);
  color: #eee;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s;
}

.input-group input:focus {
  border-color: #FFD700;
}

.input-group label {
  position: absolute;
  top: -0.6rem;
  left: 1rem;
  background: rgba(20,20,30,0.6);
  padding: 0 .4rem;
  font-size: 0.85rem;
  color: #FFD700;
}

/* بطاقات الملخص */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.card {
  display: flex;
  align-items: center;
  gap: .6rem;
  padding: 1rem;
  border-radius: 12px;
  background: rgba(255,255,255,0.05);
  box-shadow: inset 0 0 10px rgba(0,0,0,0.5),
              0 4px 12px rgba(0,0,0,0.4);
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-4px);
}

.card.correct { border-left: 4px solid #00C851; }
.card.wrong   { border-left: 4px solid #CC0000; }
.card.total   { border-left: 4px solid #33b5e5; }
.card.percent { border-left: 4px solid #ffbb33; }

.card i {
  font-size: 1.5rem;
  color: #FFD700;
}

.card .text .number {
  font-size: 1.3rem;
  font-weight: 700;
}

.card .text .desc {
  font-size: 0.85rem;
  opacity: 0.8;
}

/* الرسم */
.chart-box {
  width: 100%;
  max-width: 260px;
  height: 260px;
  margin: 0 auto 2rem;
}

/* الأزرار */
.btn {
  display: block;
  width: 100%;
  padding: 0.75rem;
  margin-bottom: 1rem;
  font-family: 'Cairo', sans-serif;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  text-align: center;
  transition: background 0.3s, transform 0.1s;
}

.btn.send {
  background: linear-gradient(90deg, #FFD700, #FFC107);
  color: #1a1a1a;
}

.btn.send:hover {
  background: linear-gradient(90deg, #FFC107, #FFEB3B);
  transform: translateY(-2px);
}

.btn.reset {
  background: #444;
  color: #eee;
}

.btn.reset:hover {
  background: #555;
  transform: translateY(-2px);
}

/* تجاوب */
@media (max-width: 480px) {
  .results-container {
    padding: 1.5rem 1rem;
  }
  .title {
    font-size: 2rem;
  }
  .chart-box { max-width: 200px; height: 200px; }
}
</style>
