const segmentData = JSON.parse(document.getElementById('segment-data').textContent);
const segmentCtx = document.getElementById('segmentChart');

new Chart(segmentCtx, {
    type: 'bar',
    data: {
        labels: segmentData.labels,
        datasets: [{
            label: 'Net Revenue ($M)',
            data: segmentData.values,
            backgroundColor: ['#00704A', '#D9822B', '#1E3932']
        }]
    },
    options: {
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            }
        },
        scales: {
            y: {
                suggestedMax: 28500
            }
        }
    }
});

const productData = JSON.parse(document.getElementById('product-data').textContent);
const productCtx = document.getElementById('productChart');

new Chart(productCtx, {
    type: 'doughnut',
    data: {
        labels: productData.labels,
        datasets: [{
            data: productData.values,
            backgroundColor: ['#00704A', '#D9822B', '#C9CDC9']
        }]
    },
    options: {
        maintainAspectRatio: false,
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return context.label + ': ' + context.raw + '%';
                    }
                }
            }
        }
    }
});

const compSalesData = JSON.parse(document.getElementById('comp-sales-data').textContent);
const compSalesCtx = document.getElementById('compSalesChart');

new Chart(compSalesCtx, {
    type: 'bar',
    data: {
        labels: compSalesData.labels,
        datasets: [{
            label: 'Global comp sales (%)',
            data: compSalesData.values,
            backgroundColor: compSalesData.values.map(v => v < 0 ? '#A33F2B' : v === 0 ? '#9CA3AF' : '#00704A')
        }]
    },
    options: {
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            }
        }
    }
});