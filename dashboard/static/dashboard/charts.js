const segmentCtx = document.getElementById('segmentChart');

new Chart(segmentCtx, {
    type: 'bar',
    data: {
        labels: ['North America', 'International', 'Channel Dev.'],
        datasets: [{
            label: 'Net Revenue ($M)',
            data: [27373.1, 7819.9, 1871.7],
            backgroundColor: ['#00704A', '#D9822B', '#1E3932']
        }]
    }
});