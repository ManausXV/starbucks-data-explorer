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

const citySearch = document.getElementById('city-search');
const countryFilter = document.getElementById('country-filter');
const ownerFilter = document.getElementById('owner-filter');
const storeRows = document.getElementById('store-rows');
const storeCount = document.getElementById('store-count');

function loadStores() {
    const params = new URLSearchParams({
        q: citySearch.value,
        country: countryFilter.value,
        owner: ownerFilter.value
    });

    fetch(`/api/stores?${params}`)
        .then(response => response.json())
        .then(data => {
            storeRows.innerHTML = '';

            data.stores.forEach(store => {
                const row = document.createElement('tr');
                [store.city, store.region, store.country, store.ownership, store.number].forEach(value => {
                    const cell = document.createElement('td');
                    cell.textContent = value;
                    row.append(cell);
                });
                storeRows.append(row);
            });

            if (data.total === 0) {
                storeCount.textContent = 'No stores match those filters.';
            } else {
                storeCount.textContent = `Showing ${data.stores.length} of ${data.total.toLocaleString()} stores`;
            }
        });
}

let searchTimer;
citySearch.addEventListener('input', () => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(loadStores, 250);
});
countryFilter.addEventListener('change', loadStores);
ownerFilter.addEventListener('change', loadStores);

loadStores();