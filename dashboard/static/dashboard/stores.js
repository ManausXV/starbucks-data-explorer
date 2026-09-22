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

const countryData = JSON.parse(document.getElementById('country-data').textContent);

new Chart(document.getElementById('countryChart'), {
    type: 'bar',
    data: {
        labels: countryData.labels,
        datasets: [{
            data: countryData.values,
            backgroundColor: '#00704A'
        }]
    },
    options: {
        indexAxis: 'y',
        maintainAspectRatio: false,
        plugins: { legend: { display: false } }
    }
});