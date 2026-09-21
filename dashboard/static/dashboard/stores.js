const countData = JSON.parse(document.getElementById('count-data').textContent);
const lastIndex = countData.values.length - 1;

new Chart(document.getElementById('countChart'), {
    type: 'bar',
    data: {
        labels: countData.labels,
        datasets: [{
            data: countData.values,
            backgroundColor: countData.values.map((v, i) => i === lastIndex ? '#00704A' : '#7FA695')
        }]
    },
    options: {
        maintainAspectRatio: false,
        plugins: { legend: { display: false } }
    }
});