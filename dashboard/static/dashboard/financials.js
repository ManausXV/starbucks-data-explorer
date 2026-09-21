
const revenueData = JSON.parse(document.getElementById('revenue-data').textContent);

new Chart(document.getElementById('revenueChart'), {
    type: 'line',
    data: {
        labels: revenueData.labels,
        datasets: [{
            data: revenueData.values,
            borderColor: '#00704A',
            backgroundColor: '#00704A',
            tension: 0.3
        }]
    },
    options: {
        maintainAspectRatio: false,
        plugins: { legend: { display: false } }
    }
});
const marginData = JSON.parse(document.getElementById('margin-data').textContent);
const yearColors = ['#C9CDC9', '#7FA695', '#00704A'];

new Chart(document.getElementById('marginChart'), {
    type: 'bar',
    data: {
        labels: marginData.labels,
        datasets: marginData.datasets.map((d, i) => ({
            label: d.label,
            data: d.values,
            backgroundColor: yearColors[i]
        }))
    },
    options: {
        maintainAspectRatio: false,
        plugins: {
            tooltip: {
                callbacks: {
                    label: function (context) {
                        return context.dataset.label + ': ' + context.raw + '%';
                    }
                }
            }
        }
    }
});
const expenseData = JSON.parse(document.getElementById('expense-data').textContent);
const costColors = ['#1E3932', '#00704A', '#7FA695', '#B7CFC2', '#A33F2B', '#D9822B'];

new Chart(document.getElementById('expenseChart'), {
    type: 'bar',
    data: {
        labels: expenseData.labels,
        datasets: expenseData.datasets.map((d, i) => ({
            label: d.label,
            data: d.values,
            backgroundColor: costColors[i]
        }))
    },
    options: {
        indexAxis: 'y',
        maintainAspectRatio: false,
        scales: {
            x: { stacked: true },
            y: { stacked: true }
        },
        plugins: {
            tooltip: {
                callbacks: {
                    label: function (context) {
                        return context.dataset.label + ': $' + context.raw.toLocaleString() + 'M';
                    }
                }
            }
        }
    }
});
const geoData = JSON.parse(document.getElementById('geo-data').textContent);

new Chart(document.getElementById('geoChart'), {
    type: 'doughnut',
    data: {
        labels: geoData.labels,
        datasets: [{
            data: geoData.values,
            backgroundColor: ['#00704A', '#1E3932', '#C9CDC9']
        }]
    },
    options: {
        maintainAspectRatio: false,
        plugins: {
            legend: { position: 'right' },
            tooltip: {
                callbacks: {
                    label: function (context) {
                        return context.label + ': ' + context.raw + '%';
                    }
                }
            }
        }
    }
});