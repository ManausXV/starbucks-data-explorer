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
    }
});