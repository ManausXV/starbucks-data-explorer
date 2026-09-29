
# Starbucks Data Explorer
A Django web app that turns eleven years of Starbucks' public financial, operational and menu data into six interactive pages. Originally built as my CS50 Web capstone project.

<img width="1269" height="638" alt="Screenshot 2026-09-29 133555" src="https://github.com/user-attachments/assets/39cb5b56-4394-496c-92ed-3d5450446566" />
<img width="1268" height="672" alt="Screenshot 2026-09-29 133703" src="https://github.com/user-attachments/assets/0e0309d7-4483-4534-8936-5e75e3d61efa" />
<img width="1267" height="671" alt="Screenshot 2026-09-29 133646" src="https://github.com/user-attachments/assets/a0b942d7-4aa8-4922-98cc-b69dc4c0d77b" />


## Live demo

[Link will be added here soon]

## Features

- **Overview** — headline figures and three feature cards linking into the rest of the site
- **Financials** — revenue trend, segment margins by year, a cost breakdown per segment, and revenue by geography, switchable by fiscal year
- **Store Growth** — store count history, top countries by store count, and a searchable directory of 28,000+ real store locations, filtered server-side
- **Menu Explorer** — a live-filterable table of 242 drinks and 113 food items, searched and sorted entirely in the browser
- **Stock & Loyalty** — ten years of quarterly share price data and US Rewards membership figures
- **Sources** — every dataset used, where it came from, and its known limitations

## Why two different filtering approaches

The store directory (28k+ rows) is filtered server-side: the browser sends a search request, the database filters it, and only 50 results come back. The menu (355 rows) is small enough to send to the browser once and filter entirely client-side, with no further requests. Same kind of feature, opposite approach, chosen by the size of the data.

## Tech stack

- Django + SQLite
- Bootstrap 4
- Chart.js
- Vanilla JavaScript, no frontend framework

## Data

Loaded from one JSON file (annual report data) and three CSVs (menu nutrition and store locations, both public Kaggle datasets) into ten Django models, via a single management command:
python manage.py load_data

It rebuilds every table from scratch, so it's safe to re-run at any time.

## Running it locally
git clone [repo url]
cd starbucks-data-explorer
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py load_data
python manage.py runserver


Then open http://127.0.0.1:8000/.

## Known limitations

- The store directory is a 2017 snapshot (28,289 stores). The FY2025 store count chart, from actual filings, says 40,990. Both are correct for their own date; the site shows both rather than hiding the gap.
- The segment cost breakdown doesn't reconcile exactly to revenue — a few smaller expense items aren't broken out in the source filings.
- Rewards membership figures are US-only, and one reading is dated only as "about 2022" in its source.

Full detail on every dataset is on the Sources page.
