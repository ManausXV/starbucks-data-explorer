const priceData = JSON.parse(document.getElementById('price-data').textContent);

new Chart(document.getElementById('priceChart'), {
    type: 'line',
    data: {
        labels: priceData.labels,
        datasets: [{
            data: priceData.values,
            borderColor: '#00704A',
            pointRadius: 2,
            tension: 0.2
        }]
    },
    options: {
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
            x: { ticks: { maxTicksLimit: 8 } }
        }
    }
});

const changeData = JSON.parse(document.getElementById('change-data').textContent);

new Chart(document.getElementById('changeChart'), {
    type: 'bar',
    data: {
        labels: changeData.labels,
        datasets: [{
            data: changeData.values,
            backgroundColor: changeData.values.map(v => v >= 0 ? '#00704A' : '#A33F2B')
        }]
    },
    options: {
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: {
                callbacks: {
                    label: function (context) {
                        return context.label + ': ' + context.raw + '%';
                    }
                }
            }
        },
        scales: {
            x: { ticks: { maxTicksLimit: 8 } }
        }
    }
});

const loyaltyData = JSON.parse(document.getElementById('loyalty-data').textContent);

new Chart(document.getElementById('loyaltyChart'), {
    type: 'bar',
    data: {
        labels: loyaltyData.labels,
        datasets: [{
            data: loyaltyData.values,
            backgroundColor: loyaltyData.labels.map(label => label.includes('~') ? '#C9CDC9' : '#00704A')
        }]
    },
    options: {
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: {
                callbacks: {
                    label: function (context) {
                        return context.raw + 'M members';
                    }
                }
            }
        }
    }
});