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
        <label for="teacherPhone">رقم المدرس (مثال: 0988131514)</label>
      </div>
    </div>

    <!-- زر إرسال واتساب -->
    <div v-if="studentNameValid && teacherPhoneValid" class="action-btns">
      <button class="btn whatsapp" @click="sendReportToTeacher">
        <i class="fab fa-whatsapp fa-lg" style="margin-left: 8px;"></i>
        إرسال النتيجة عبر واتساب
      </button>
    </div>

    <!-- بطاقات النتائج -->
    <div class="cards-grid">
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
    <div class="chart-box">
      <canvas ref="doughnutCanvas"></canvas>
    </div>

    <!-- زر إعادة -->
    <button class="btn reset" @click="$emit('reset')">
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
    correct: { type: Number, required: true },
    wrong: { type: Number, required: true },
    percentage: { type: Number, required: true }
  },
  setup(props) {
    const studentName = ref('')
    const teacherPhone = ref('')
    const doughnutCanvas = ref(null)

    const total = computed(() => props.correct + props.wrong)
    const studentNameValid = computed(() => studentName.value.trim().length > 0)
    const teacherPhoneValid = computed(() => /^[0-9]{10}$/.test(teacherPhone.value.trim()))

    const sendReportToTeacher = () => {
      const text = encodeURIComponent(
        `📘 *نتائج اختبار الطالب*\n\n` +
        `👤 *الاسم:* ${studentName.value}\n` +
        `✅ *إجابات صحيحة:* ${props.correct}\n` +
        `❌ *إجابات خاطئة:* ${props.wrong}\n` +
        `📊 *النسبة المئوية:* ${props.percentage}%\n` +
        `🔢 *الإجمالي:* ${total.value}`
      )
      const phoneNumber = teacherPhone.value.startsWith('0')
        ? teacherPhone.value.replace(/^0/, '966')
        : teacherPhone.value

      window.open(`https://wa.me/${phoneNumber}?text=${text}`, '_blank')
    }

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
            borderWidth: 3,
            borderColor: '#2f2f40'
          }]
        },
        options: {
          cutout: '70%',
          animation: {
            duration: 1500,
            easing: 'easeOutBounce'
          },
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

    onMounted(renderChart)
    watch([() => props.correct, () => props.wrong], renderChart)

    return {
      studentName, teacherPhone,
      studentNameValid, teacherPhoneValid,
      doughnutCanvas, total,
      sendReportToTeacher
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css');

.results-container {
  max-width: 750px;
  margin: 3rem auto;
  padding: 2.5rem;
  border-radius: 20px;
  background: linear-gradient(145deg, #1a1a2e, #16213e);
  color: #f1f1f1;
  font-family: 'Cairo', sans-serif;
  box-shadow: 0 20px 50px rgba(0,0,0,0.6);
  text-align: center;
}

.title {
  font-size: 2.8rem;
  font-weight: 900;
  margin-bottom: 2rem;
  background: linear-gradient(to right, #00E676, #00BFA5);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Inputs */
.inputs-wrapper {
  display: grid;
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}

.input-group {
  position: relative;
}

.input-group input {
  width: 100%;
  padding: 1rem;
  border: 2px solid #555;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.07);
  color: #fff;
  font-size: 1rem;
  transition: 0.3s;
}

.input-group input:focus {
  border-color: #00E676;
}

.input-group label {
  position: absolute;
  top: -0.7rem;
  left: 1rem;
  background: #16213e;
  padding: 0 .5rem;
  font-size: 0.85rem;
  color: #00E676;
}

/* Cards */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 1.2rem;
  margin-bottom: 2.5rem;
}

.card {
  display: flex;
  align-items: center;
  gap: .8rem;
  padding: 1rem;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.05);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-3px);
}

.card.correct { border-left: 4px solid #00E676; }
.card.wrong   { border-left: 4px solid #F44336; }
.card.total   { border-left: 4px solid #03A9F4; }
.card.percent { border-left: 4px solid #FFC107; }

.card i {
  font-size: 1.6rem;
  color: #fff176;
}

.card .text .number {
  font-size: 1.5rem;
  font-weight: 800;
}

.card .text .desc {
  font-size: 0.9rem;
  opacity: 0.85;
}

/* الرسم */
.chart-box {
  width: 100%;
  max-width: 300px;
  height: 300px;
  margin: 0 auto 2.5rem;
}

/* أزرار */
.action-btns {
  margin-bottom: 2rem;
}

.btn {
  width: 100%;
  padding: 1rem;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 800;
  cursor: pointer;
  transition: 0.3s;
}

.btn.whatsapp {
  background: linear-gradient(90deg, #25D366, #128C7E);
  color: white;
}

.btn.whatsapp:hover {
  background: linear-gradient(90deg, #1ebe5d, #0f7c6c);
  transform: scale(1.02);
}

.btn.reset {
  background: #444;
  color: #eee;
}

.btn.reset:hover {
  background: #555;
  transform: scale(1.02);
}

/* تجاوب */
@media (max-width: 480px) {
  .results-container {
    padding: 1.5rem;
  }
  .title {
    font-size: 2rem;
  }
  .chart-box {
    max-width: 200px;
    height: 200px;
  }
}
</style>