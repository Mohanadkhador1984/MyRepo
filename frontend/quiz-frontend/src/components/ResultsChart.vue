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
          placeholder="أدخل اسم الطالب"
          :disabled="sent"
        />
        <label for="studentName">اسم الطالب</label>
      </div>

      <div class="input-group">
        <input
          id="teacherPhone"
          v-model="teacherPhone"
          type="tel"
          placeholder="مثال: 0988131514"
          :disabled="sent"
        />
        <label for="teacherPhone">رقم المدرّس</label>
      </div>
    </div>

    <!-- زر إرسال واتساب -->
    <div class="action-btns">
      <button
        class="btn whatsapp"
        :disabled="!canSend || sent"
        @click="sendReportToTeacher"
      >
        <i class="fab fa-whatsapp fa-lg"></i>
        {{ sent ? 'تم الإرسال' : 'إرسال النتيجة عبر واتساب' }}
      </button>
    </div>

    <!-- بطاقات النتائج -->
    <div class="cards-grid" :class="{ locked: sent }">
      <div class="card correct">
        <i class="fas fa-check-circle"></i>
        <div class="text">
          <span class="number">{{ correct }}</span>
          <span class="desc">إجابات صحيحة</span>
        </div>
      </div>
      <div class="card wrong">
        <i class="fas fa-times-circle"></i>
        <div class="text">
          <span class="number">{{ wrong }}</span>
          <span class="desc">إجابات خاطئة</span>
        </div>
      </div>
      <div class="card total">
        <i class="fas fa-layer-group"></i>
        <div class="text">
          <span class="number">{{ total }}</span>
          <span class="desc">الإجمالي</span>
        </div>
      </div>
      <div class="card percent">
        <i class="fas fa-chart-pie"></i>
        <div class="text">
          <span class="number">{{ percentage }}%</span>
          <span class="desc">النسبة المئوية</span>
        </div>
      </div>
    </div>

    <!-- الرسم الدائري -->
    <div class="chart-box" :class="{ locked: sent }">
      <canvas ref="doughnutCanvas"></canvas>
    </div>

    <!-- زر إعادة الاختبار -->
    <button
      class="btn reset"
      @click="$emit('reset')"
      :disabled="!sent"
    >
      إعادة الاختبار
    </button>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import Chart from 'chart.js/auto'

export default {
  name: 'ResultsChartModern',
  props: {
    correct:    { type: Number, required: true },
    wrong:      { type: Number, required: true },
    percentage: { type: Number, required: true }
  },
  setup(props) {
    const studentName    = ref('')
    const teacherPhone   = ref('')
    const sent           = ref(false)
    const doughnutCanvas = ref(null)

    const total = computed(() => props.correct + props.wrong)
    const studentNameValid = computed(() =>
      studentName.value.trim().length > 0
    )
    const teacherPhoneValid = computed(() =>
      /^09\d{8}$/.test(teacherPhone.value.trim())
    )
    const canSend = computed(() =>
      studentNameValid.value && teacherPhoneValid.value && !sent.value
    )

    // eslint-disable-next-line no-unused-vars
    const isPass = computed(() => props.percentage >= 50)

    const renderChart = () => {
      if (!doughnutCanvas.value) return
      new Chart(doughnutCanvas.value, {
        type: 'doughnut',
        data: {
          labels: ['صحيحة', 'خاطئة'],
          datasets: [{
            data: [props.correct, props.wrong],
            backgroundColor: ['#00E676', '#F44336'],
            hoverBackgroundColor: ['#00C853', '#E53935'],
            borderColor: '#2f2f40',
            borderWidth: 3
          }]
        },
        options: {
          cutout: '70%',
          animation: {
            duration: 1500,
            easing: 'easeOutBounce'
          },
          plugins: {
            legend: { display: false }
          }
        }
      })
    }

    // إرسال مباشر عبر الباك-إند دون معاينة WhatsApp
    const sendReportToTeacher = async () => {
      if (!canSend.value) return

      sent.value = true

      const payload = {
        phone:      teacherPhone.value.trim(),
        name:       studentName.value.trim(),
        correct:    props.correct,
        wrong:      props.wrong,
        percentage: props.percentage
      }

      try {
        await fetch('/api/send-whatsapp', {
          method:  'POST',
          headers: { 'Content-Type': 'application/json' },
          body:    JSON.stringify(payload)
        })
        // يمكنك هنا التعامل مع رد السيرفر أو عرض إشعار نجاح
      }
      catch (err) {
        console.error('Send failed:', err)
        sent.value = false
      }
    }

    onMounted(renderChart)
    watch([() => props.correct, () => props.wrong], renderChart)

    return {
      studentName,
      teacherPhone,
      canSend,
      sendReportToTeacher,
      doughnutCanvas,
      total,
      sent
    }
  }
}
</script>

<style scoped>
/* eslint-disable */
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css');

.results-container {
  max-width: 650px;
  margin: 3rem auto;
  padding: 2rem;
  background: linear-gradient(145deg, #1f1f35, #161626);
  color: #f1f1f1;
  font-family: 'Cairo', sans-serif;
  text-align: center;
  border-radius: 16px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.6);
}


.title {
  font-size: 2.4rem;
  font-weight: 900;
  margin-bottom: 1.5rem;
  background: linear-gradient(to right, #00E676, #00BFA5);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.inputs-wrapper {
  margin-bottom: 2rem;
}
.input-group {
  position: relative;
  width: 100%;
  margin-bottom: 1rem;
}
.input-group input {
  width: 100%;
  padding: 0.9rem 1rem;
  border: 2px solid #444;
  border-radius: 12px;
  background: rgba(255,255,255,0.05);
  color: #fff;
  font-size: 1rem;
  transition: border-color 0.3s;
}
.input-group input:focus {
  border-color: #00E676;
  outline: none;
}
.input-group label {
  position: absolute;
  top: -0.7rem;
  left: 1rem;
  background: #161626;
  padding: 0 0.5rem;
  font-size: 0.85rem;
  color: #00E676;
}

.action-btns {
  margin-bottom: 2rem;
}
.btn.whatsapp {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(90deg, #25D366, #128C7E);
  color: #fff;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  cursor: pointer;
  box-shadow: 0 8px 20px rgba(37,211,102,0.4);
  transition: background 0.3s, transform 0.2s;
}
.btn.whatsapp:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.btn.whatsapp:not(:disabled):hover {
  transform: translateY(-2px);
  background: linear-gradient(90deg, #1ebe5d, #0f7c6c);
}

.cards-grid,
.chart-box {
  opacity: 1;
  transition: opacity 0.3s;
}
.cards-grid.locked,
.chart-box.locked {
  opacity: 0.6;
  pointer-events: none;
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
  padding: 1rem;
  background: rgba(255,255,255,0.05);
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.3);
  transition: transform 0.2s;
}
.card:hover { transform: translateY(-4px); }
.card.correct { border-left: 4px solid #00E676; }
.card.wrong   { border-left: 4px solid #F44336; }
.card.total   { border-left: 4px solid #03A9F4; }
.card.percent { border-left: 4px solid #FFC107; }
.card i {
  font-size: 1.6rem;
  color: #fff176;
}
.card .text .number {
  font-size: 1.4rem;
  font-weight: 800;
}
.card .text .desc {
  font-size: 0.9rem;
  opacity: 0.85;
}

.chart-box {
  width: 100%;
  max-width: 300px;
  height: 300px;
  margin: 0 auto 2rem;
}

.btn.reset {
  width: 100%;
  padding: 1rem;
  background: #444;
  color: #eee;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 700;
  box-shadow: 0 6px 16px rgba(0,0,0,0.4);
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
}
.btn.reset:hover {
  background: #555;
  transform: translateY(-2px);
}

@media (max-width: 480px) {
  .results-container { padding: 1.5rem; }
  .title { font-size: 2rem; }
  .chart-box { max-width: 200px; height: 200px; }
}
</style>
