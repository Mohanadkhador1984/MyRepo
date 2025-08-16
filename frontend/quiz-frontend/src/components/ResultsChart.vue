<!-- src/components/ResultsChart.vue -->
<template>
  <div class="results-chart-container">

    <!-- عنوان -->
    <h2 class="title">نتائج الاختبار</h2>

    <!-- حقل إدخال اسم الطالب -->
    <div class="input-group">
      <label for="studentName">اسم الطالب</label>
      <input
        id="studentName"
        v-model="studentName"
        type="text"
        placeholder="أدخل اسم الطالب"
      />
    </div>

    <!-- بطاقات الملخص -->
    <div class="metrics-grid">
      <div class="metric-card correct-card">
        <i class="fas fa-check-circle icon"></i>
        <div class="metric-info">
          <span class="num">{{ correct }}</span>
          <span class="label">إجابات صحيحة</span>
        </div>
      </div>
      <div class="metric-card wrong-card">
        <i class="fas fa-times-circle icon"></i>
        <div class="metric-info">
          <span class="num">{{ wrong }}</span>
          <span class="label">إجابات خاطئة</span>
        </div>
      </div>
      <div class="metric-card total-card">
        <i class="fas fa-list-ol icon"></i>
        <div class="metric-info">
          <span class="num">{{ total }}</span>
          <span class="label">إجمالي الأسئلة</span>
        </div>
      </div>
      <div class="metric-card percent-card">
        <i class="fas fa-percentage icon"></i>
        <div class="metric-info">
          <span class="num">{{ percentage }}%</span>
          <span class="label">نسبة النجاح</span>
        </div>
      </div>
    </div>

    <!-- الرسم الدائري -->
    <div class="chart-wrapper">
      <canvas ref="doughnutCanvas"></canvas>
    </div>

    <!-- زر إرسال عبر واتساب -->
    <button
      class="send-btn"
      :disabled="!studentName"
      @click="sendWhatsAppReport"
    >
      إرسال عبر واتساب
    </button>

    <!-- زر إعادة الاختبار -->
    <button class="reset-btn" @click="$emit('reset')">
      إعادة الاختبار
    </button>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import Chart from 'chart.js/auto'

export default {
  name: 'ResultsChart',
  props: {
    correct:    { type: Number, required: true },
    wrong:      { type: Number, required: true },
    percentage: { type: Number, required: true }
  },
  setup(props) {
    const doughnutCanvas = ref(null)
    const studentName = ref('')
    const whatsappNumber = '+963953447860'  // رقم المستلم
    let chartInstance = null

    const total = props.correct + props.wrong

    const renderChart = () => {
      if (chartInstance) chartInstance.destroy()
      chartInstance = new Chart(doughnutCanvas.value, {
        type: 'doughnut',
        data: {
          labels: ['صحيحة', 'خاطئة'],
          datasets: [{
            data: [props.correct, props.wrong],
            backgroundColor: ['#10b981', '#ef4444'],
            hoverBackgroundColor: ['#059669', '#dc2626'],
            borderWidth: 0
          }]
        },
        options: {
          cutout: '70%',
          plugins: {
            tooltip: {
              callbacks: {
                label(context) {
                  return `${context.label}: ${context.parsed} (${Math.round((context.parsed/total)*100)}%)`
                }
              }
            },
            legend: { display: false }
          }
        }
      })
    }

    const sendWhatsAppReport = () => {
      const msg = encodeURIComponent(
        `نتائج الاختبار للطالب: ${studentName.value}\n` +
        `✅ إجابات صحيحة: ${props.correct}\n` +
        `❌ إجابات خاطئة: ${props.wrong}\n` +
        `📊 نسبة النجاح: ${props.percentage}%\n` +
        `📋 إجمالي الأسئلة: ${total}`
      )
      window.open(
        `https://api.whatsapp.com/send?phone=${whatsappNumber}&text=${msg}`,
        '_blank'
      )
    }

    onMounted(renderChart)
    watch([() => props.correct, () => props.wrong], renderChart)

    return {
      doughnutCanvas,
      studentName,
      total,
      sendWhatsAppReport
    }
  }
}
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css');
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600&display=swap');

.results-chart-container {
  font-family: 'Cairo', sans-serif;
  max-width: 600px;
  margin: 2rem auto;
  background: #fff;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  text-align: center;
}

.title {
  font-size: 1.6rem;
  margin-bottom: 1rem;
  color: #111827;
}

.input-group {
  margin-bottom: 1rem;
  text-align: left;
}
.input-group label {
  display: block;
  font-size: 0.9rem;
  color: #4b5563;
  margin-bottom: 0.25rem;
}
.input-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 1rem;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.metric-card {
  display: flex;
  align-items: center;
  background: #f9fafb;
  border-radius: 8px;
  padding: 0.75rem;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}
.metric-card.correct-card { background: #d1fae5; }
.metric-card.wrong-card   { background: #fee2e2; }
.metric-card.total-card   { background: #e0f2fe; }
.metric-card.percent-card { background: #fefce8; }

.icon {
  font-size: 1.8rem;
  margin-right: 0.75rem;
  color: #4b5563;
}

.metric-info .num {
  display: block;
  font-size: 1.4rem;
  font-weight: 600;
  color: #111827;
}
.metric-info .label {
  font-size: 0.9rem;
  color: #4b5563;
}

.chart-wrapper {
  position: relative;
  width: 200px;
  height: 200px;
  margin: 0 auto 1.5rem;
}

.send-btn {
  background: #10b981;
  color: #fff;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.2s;
  margin-bottom: 0.5rem;
}
.send-btn:disabled {
  background: #a7f3d0;
  cursor: not-allowed;
}
.send-btn:hover:not(:disabled) {
  background: #059669;
}

.reset-btn {
  background: #2563eb;
  color: #fff;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.2s;
}
.reset-btn:hover {
  background: #1e40af;
}
</style>
