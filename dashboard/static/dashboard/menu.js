const drinks = JSON.parse(document.getElementById('drinks-data').textContent);
const foods = JSON.parse(document.getElementById('foods-data').textContent);

const tableHead = document.getElementById('menu-head');
const tableBody = document.getElementById('menu-rows');
const searchInput = document.getElementById('menu-search');
const categorySelect = document.getElementById('menu-category');
const sortSelect = document.getElementById('menu-sort');
const menuCount = document.getElementById('menu-count');

const drinksButton = document.getElementById('mode-drinks');
const foodsButton = document.getElementById('mode-foods');
const categoryWrapper = document.getElementById('category-wrapper');

const drinkColumns = [
    { key: 'beverage', label: 'Drink' },
    { key: 'category', label: 'Category' },
    { key: 'prep', label: 'Size / milk' },
    { key: 'calories', label: 'Calories', sortable: true },
    { key: 'sugars', label: 'Sugar (g)', sortable: true },
    { key: 'caffeine', label: 'Caffeine (mg)', sortable: true },
];
const foodColumns = [
    { key: 'name', label: 'Item' },
    { key: 'calories', label: 'Calories', sortable: true },
    { key: 'fat', label: 'Fat (g)', sortable: true },
    { key: 'carbs', label: 'Carbs (g)', sortable: true },
    { key: 'protein', label: 'Protein (g)', sortable: true },
];

function renderTable(columns, items) {
    tableHead.innerHTML = '';
    const headerRow = document.createElement('tr');
    columns.forEach(col => {
        const th = document.createElement('th');
        th.textContent = col.label;
        headerRow.append(th);
    });
    tableHead.append(headerRow);

    tableBody.innerHTML = '';
    items.forEach(item => {
        const row = document.createElement('tr');
        columns.forEach(col => {
            const cell = document.createElement('td');
            const value = item[col.key];
            cell.textContent = value === null ? '—' : value;
            row.append(cell);
        });
        tableBody.append(row);
    });
}

function setMode(newMode) {
    mode = newMode;

    drinksButton.classList.toggle('active', mode === 'drinks');
    foodsButton.classList.toggle('active', mode === 'foods');
    categoryWrapper.classList.toggle('d-none', mode !== 'drinks');

    searchInput.value = '';
    categorySelect.value = '';
    fillSortOptions(mode === 'drinks' ? drinkColumns : foodColumns);

    update();
}

drinksButton.addEventListener('click', () => setMode('drinks'));
foodsButton.addEventListener('click', () => setMode('foods'));

function fillSortOptions(columns) {
    sortSelect.innerHTML = '';

    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = 'Menu order';
    sortSelect.append(defaultOption);

    columns.filter(col => col.sortable).forEach(col => {
        const option = document.createElement('option');
        option.value = col.key;
        option.textContent = col.label + ', highest first';
        sortSelect.append(option);
    });
}

const categories = [...new Set(drinks.map(d => d.category))].sort();
categories.forEach(cat => {
    const option = document.createElement('option');
    option.value = cat;
    option.textContent = cat;
    categorySelect.append(option);
});

fillSortOptions(drinkColumns);
let mode = 'drinks';

function update() {
    const isDrinks = mode === 'drinks';
    const items = isDrinks ? drinks : foods;
    const columns = isDrinks ? drinkColumns : foodColumns;
    const nameKey = isDrinks ? 'beverage' : 'name';

    const query = searchInput.value.toLowerCase();
    const category = categorySelect.value;

    const results = items.filter(item =>
        item[nameKey].toLowerCase().includes(query) &&
        (!isDrinks || category === '' || item.category === category)
    );

    const sortKey = sortSelect.value;
    if (sortKey !== '') {
        results.sort((a, b) => (b[sortKey] ?? -1) - (a[sortKey] ?? -1));
    }

    renderTable(columns, results);
    menuCount.textContent = `Showing ${results.length} of ${items.length} ${isDrinks ? 'drinks' : 'items'}`;
}

searchInput.addEventListener('input', update);
categorySelect.addEventListener('change', update);
sortSelect.addEventListener('change', update);

update();