<template>
  <div class="results-container" ref="resultsContainer">

    <!-- زر الإغلاق الفاخر -->
    <button
      type="button"
      class="close-btn"
      @click="$emit('reset')"
      aria-label="إغلاق"
    >
      <i class="fas fa-times fa-lg"></i>
    </button>

    <!-- العنوان -->
    <h2 class="title">نتائج الاختبار</h2>

    <!-- حقول الإدخال -->
    <div class="inputs-wrapper">
      <!-- اسم الطالب -->
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

      <!-- رقم المدرّس مع أيقونة اختيار من جهات الاتصال داخل الحقل -->
      <div class="input-group">
        <input
          id="teacherPhone"
          v-model="teacherPhone"
          type="tel"
          inputmode="tel"
          pattern="09[0-9]{8}"
          placeholder="مثال: 0991234567"
          :disabled="sent"
        />
        <!-- أيقونة اختيار جهة الاتصال -->
        <i
          v-if="canPickContact && !sent"
          type="button"
          class="fas fa-address-book pick-icon"
          @click="pickContact"
          aria-label="اختر رقم من جهات الاتصال"
        ></i>
        <label for="teacherPhone">رقم المدرّس (09xxxxxxx)</label>
      </div>
    </div>

    <!-- زر إرسال واتساب -->
    <div class="action-btns">
      <button
        type="button"
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

    <!-- زر إعادة الاختبار (أحمر فاقع) -->
    <button
      type="button"
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
import html2canvas from 'html2canvas'

export default {
  name: 'ResultsChartModern',
  props: {
    correct:    { type: Number, required: true },
    wrong:      { type: Number, required: true },
    percentage: { type: Number, required: true }
  },
  setup(props) {
    const studentName      = ref('')
    const teacherPhone     = ref('')
    const sent             = ref(false)
    const doughnutCanvas   = ref(null)
    const resultsContainer = ref(null)

    const total = computed(() => props.correct + props.wrong)

    // Syrian numbers: local 09xxxxxxxx or with +9639xxxxxxxx
    const teacherPhoneValid = computed(() => /^09\d{8}$/.test(teacherPhone.value.trim()))
    const studentNameValid = computed(() => studentName.value.trim().length > 0)
    const canSend = computed(() =>
      studentNameValid.value && teacherPhoneValid.value && !sent.value
    )

    // Contact Picker support
    const canPickContact = 'contacts' in navigator && 'select' in navigator.contacts

    async function pickContact() {
      try {
        const contacts = await navigator.contacts.select(['tel'], { multiple: false })
        if (contacts.length && contacts[0].tel.length) {
          let num = contacts[0].tel[0].replace(/\s+/g, '')
          // Normalize +9639... or 9639... to local 09...
          if (num.startsWith('+963')) num = '0' + num.slice(4)
          else if (num.startsWith('963')) num = '0' + num.slice(3)
          teacherPhone.value = num
        }
      } catch {
        // ignore user cancel or unsupported
      }
    }

    function renderChart() {
      if (!doughnutCanvas.value) return
      new Chart(doughnutCanvas.value, {
        type: 'doughnut',
        data: {
          labels: ['صحيحة','خاطئة'],
          datasets: [{
            data: [props.correct, props.wrong],
            backgroundColor: ['#00E676','#F44336'],
            hoverBackgroundColor: ['#00C853','#E53935'],
            borderColor: '#2f2f40',
            borderWidth: 3
          }]
        },
        options: { cutout: '70%' }
      })
    }

    async function sendReportToTeacher() {
      if (!canSend.value) return
      sent.value = true

      const payload = {
        phone:      teacherPhone.value.trim(),
        name:       studentName.value.trim(),
        correct:    props.correct,
        wrong:      props.wrong,
        percentage: props.percentage
      }

      const lines = [
        '📊 *نتائج اختبار الطالب* 📊',
        '',
        `👤 *الاسم:* ${payload.name}`,
        `✅ *صحيحة:* ${payload.correct}`,
        `❌ *خاطئة:* ${payload.wrong}`,
        `🔢 *المجموع:* ${payload.correct + payload.wrong}`,
        `📈 *النسبة:* ${payload.percentage}%`,
        '',
        payload.percentage >= 50
          ? '🎉 *مبروك* على النجاح! 🚀'
          : '💪 *لا تيأس*! المحاولة القادمة أفضل. 🌟'
      ]
      const formattedMsg = lines.join('\n')

      // Try Web Share API with image
      if (navigator.canShare && navigator.canShare({ files: [] })) {
        try {
          const canvas = await html2canvas(resultsContainer.value, { scale: 2 })
          const blob = await new Promise(res => canvas.toBlob(res, 'image/png'))
          const file = new File([blob], 'result.png', { type: 'image/png' })
          await navigator.share({ files: [file], text: formattedMsg })
          return
        } catch {
          /* fallback */
        }
      }

      // Fallback wa.me
      window.open(
        `https://wa.me/${payload.phone}?text=${encodeURIComponent(formattedMsg)}`,
        '_blank'
      )
    }

    onMounted(renderChart)
    watch([() => props.correct, () => props.wrong], renderChart)

    return {
      studentName,
      teacherPhone,
      sent,
      total,
      canSend,
      canPickContact,
      pickContact,
      sendReportToTeacher,
      doughnutCanvas,
      resultsContainer
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css');

/* ضع أنماطك الأصلية هنا */

.input-group {
  position: relative;
}
.pick-icon {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.2rem;
  color: #ccc;
  cursor: pointer;
  transition: color 0.2s;
}
.pick-icon:hover {
  color: #fff;
}

/* وأبقي باقي الأنماط كما هي سابقاً */
</style>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css');

/* preserve your existing styles… */

.inputs-wrapper .pick-contact {
  margin-top: 0.5rem;
  width: 100%;
  padding: 0.8rem;
  background: #304ffe;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
}
.inputs-wrapper .pick-contact:hover {
  background: #1e40ff;
  transform: translateY(-2px);
}

.results-container {
  position: relative;
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

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 3rem;
  height: 3rem;
  background: linear-gradient(145deg, #ffdd00, #e6c200);
  border: 2px solid #fff8c6;
  border-radius: 50%;
  box-shadow:
    0 0 8px rgba(255,221,0,0.6),
    0 0 20px rgba(230,194,0,0.4),
    inset 0 0 10px rgba(255,255,255,0.5);
  color: #ffffff;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.3s;
}

.close-btn::before {
  content: "";
  position: absolute;
  top: -10%;
  left: -10%;
  width: 120%;
  height: 120%;
  background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.4), transparent 70%);
  transform: rotate(45deg);
  pointer-events: none;
}

.close-btn:hover {
  transform: scale(1.2);
  box-shadow:
    0 0 12px rgba(255,221,0,0.8),
    0 0 30px rgba(230,194,0,0.6),
    inset 0 0 15px rgba(255,255,255,0.7);
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
  background: #e53935; /* أحمر فاقع */
  color: #fff;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 700;
  box-shadow: 0 6px 16px rgba(0,0,0,0.4);
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
}
.btn.reset:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.btn.reset:hover:not(:disabled) {
  background: #d32f2f;
  transform: translateY(-2px);
}

@media (max-width: 480px) {
  .results-container { padding: 1.5rem; }
  .title { font-size: 2rem; }
  .chart-box { max-width: 200px; height: 200px; }
}
</style>
