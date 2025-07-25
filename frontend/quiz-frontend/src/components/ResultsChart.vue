<template>
  <div class="report-screen">
    <h1>التقرير النهائي</h1>
    <div class="results-grid">
      <div><h5>إجابات صحيحة</h5><p>{{ correct }}</p></div>
      <div><h5>إجابات خاطئة</h5><p>{{ wrong }}</p></div>
      <div><h5>نسبة النجاح</h5><p>{{ percentage }}%</p></div>
    </div>
    <canvas ref="chart"></canvas>
    <a :href="waLink" target="_blank">شارك على واتساب</a>
    <button @click="$emit('reset')">إعادة</button>
  </div>
</template>
<script>
import Chart from 'chart.js/auto'
export default {
  name: 'ResultsChart',
  props: { correct: Number, wrong: Number, percentage: Number },
  computed: {
    waLink() {
      const msg = `✅${this.correct} ❌${this.wrong} 🏆${this.percentage}%`
      return `https://wa.me/?text=${encodeURIComponent(msg)}`
    }
  },
  mounted() {
    const ctx = this.$refs.chart.getContext('2d')
    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['صح','خطأ'],
        datasets: [{ data:[this.correct, this.wrong],
          backgroundColor:['#8cf29b','#ff8c8c'] }]
      },
      options: { cutout: '70%' }
    })
  }
}
</script>
