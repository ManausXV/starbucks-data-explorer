# Starbucks Data Explorer

A Django web application for exploring Starbucks' financial, operational and menu
data. It takes eleven years of figures from annual reports, plus three public
datasets, and presents them as six interactive pages.

Live data covers total revenue (FY2015 to FY2025), segment profit and costs,
store growth, the full drinks and food menu, quarterly share prices, and US
Rewards membership.

## Distinctiveness and Complexity

Every other project in this course is a CRUD application built around user
accounts. Wiki, Commerce, Mail and Network all follow the same shape, where
a user signs in, creates content, edits it, and deletes it, and the main work
work lies in managing the content and the permissions regarding it. My project
does not have any authentication, user accounts, and no user-generated content of any
kind. It is read-only by design. Its purpose is to take a bunch of real data
and present it in a way that someone can actually reason about it. That
makes it a different class of application rather than a variation on the same one,
and it means the difficulty sits in completely different places: in getting messy
real-world data into a usable and readable shape, in choosing how to query it efficiently, and
in presenting figures honestly when the sources disagree with each other.

The data pipeline is the base of the project. The command, `load_data`, reads
one JSON file and three CSV files and distributes that data among a few
database tables. The raw sources are not clean either. Some CSVs are encoded in UTF-16
while the others are UTF-8, so opening them the same way is not possible. Several
column headers carry stray leading or trailing whitespace, which means the obvious
lookup misses. Caffeine values in the drinks data sometimes read "Varies" instead
of a number, which can not be converted to a float, so a helper function catches
that and stores a null rather than crashing or inventing a zero. The financial
JSON nests segment data by fiscal year rather than storing a flat list, so loading
it needs a nested loop and a mapping from the file's internal keys to readable
segment names. The command clears every table before reloading, so it can be run
repeatedly without producing duplicates, and the entire database can be rebuilt
from the original files at any time.

The most significant technical decision in the project is that searching works in
two completely different ways, and each is chosen for a reason. The store
directory searches 28,289 rows. Sending that many records to the browser would be
wasteful and slow, so the page instead calls a dedicated endpoint that returns
JSON rather than HTML. The database applies the filters and returns the first
fifty matches, along with a total count so the page can report how many results
exist beyond the ones shown. Because that request travels to the server, typing
would otherwise fire one request per keystroke, so the search input is debounced:
each keystroke cancels the pending request and schedules a new one, meaning a
search only runs once the user pauses. The menu explorer faces the same problem
with a dataset of only 355 items. There, the opposite approach is correct, so the
entire menu is delivered once with the page and every subsequent search, category
filter and sort happens in the browser with no further requests at all. The same
feature is implemented twice in opposite directions, and the deciding factor is
the size of the underlying data.

Work is also pushed into the database wherever it belongs there. The top countries
chart needs to know which ten countries have the most stores out of 28,289 rows.
Rather than loading every row into Python and counting them in a loop, the query
groups by country, counts each group, sorts by that count and takes the top ten,
all in a single database query using `values()`, `annotate()` and `Count`. The
database returns ten small rows instead of nearly thirty thousand. The same
thinking applies throughout: aggregate figures are calculated by the database, and
Python only handles what remains.

The part of this project I am most confident about is how it handles data that
does not agree with itself. The searchable store directory comes from a dataset
compiled around 2017 and contains 28,289 stores, while the FY2025 annual report
states there are 40,990. Both numbers are accurate for their own point in time,
and roughly 12,700 stores opened in between. Rather than hiding one figure or
quietly picking whichever looked better, the site shows both and explains the gap
directly on the page where the conflict appears. The Rewards membership data has a
similar problem: one of the nine readings is dated only as "about 2022" in its
source. It is kept, but drawn in grey and never used to calculate growth, and the
chart uses bars rather than a line specifically because the readings are unevenly
spaced and a line would imply measurements that were never taken. The segment cost
breakdown does not reconcile exactly to revenue, because Starbucks reports only
five expense lines per segment while a few smaller items sit outside them, and the
site states that rather than forcing the numbers to add up. An entire page is
dedicated to documenting where every figure came from, how much confidence it
deserves, and what it cannot be used to argue. Building something that presents
real data without overstating it turned out to be a harder and more interesting
problem than any individual technical feature in the project.

## Files

### Application code

- **`dashboard/models.py`** defines ten models: `FinancialYear`,
  `SegmentPerformance`, `ProductRevenue`, `GeographyRevenue`, `StoreCountYear`,
  `StockQuarter`, `LoyaltyQuarter`, `MenuDrink`, `MenuFood` and `StoreLocation`.
  Fields that are genuinely missing in the source data are nullable, so gaps stay
  visible rather than being silently filled with zeros.

- **`dashboard/views.py`** holds one view per page, plus `store_search`, which
  returns JSON rather than HTML. It also defines the country and ownership code
  lookups and the Sources page content.

- **`dashboard/urls.py`** maps seven routes: the six pages and the search
  endpoint.

- **`dashboard/admin.py`** registers all ten models so the loaded data can be
  inspected through Django's admin interface.

- **`dashboard/management/commands/load_data.py`** is a custom management command
  that reads the raw files and populates every table. Run with
  `python manage.py load_data`.

### Templates

- **`layout.html`** is the base template: navigation, stylesheets, and the script
  tags for Chart.js. It defines `body` and `scripts` blocks, kept separate so each
  page's JavaScript loads after the charting library.
- **`index.html`** is the Overview page: headline figures, three feature cards and
  three charts.
- **`financials.html`** covers revenue trend, margin comparison, segment cards,
  cost breakdown and geography, with fiscal year selected through the URL.
- **`stores.html`** covers store growth, top countries and the searchable store
  directory.
- **`menu.html`** is the menu explorer, with a drinks and food toggle.
- **`stock.html`** covers share price and Rewards membership.
- **`sources.html`** documents every dataset and the site's known limitations.

### Static files

- **`style.css`** holds only what Bootstrap does not provide: brand colours, the
  stat and chart card styles, the hero layout and fixed chart heights.
- **`charts.js`**, **`financials.js`**, **`stores.js`**, **`menu.js`** and
  **`stock.js`** each hold the chart and interaction code for one page.
- **`images/`** holds the three photographs used on the Overview cards.

### Data

- **`dashboard/data/`** holds the raw sources: `starbucks_data_v3.json` for all
  figures taken from annual reports, and three CSV files covering drink
  nutrition, food nutrition and store locations.

## Running the application
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py load_data
python manage.py runserver


Then open `http://127.0.0.1:8000/`. The `load_data` step is required; without it
the database exists but every page will be empty.

To browse the data directly, create an admin account with
`python manage.py createsuperuser` and visit `/admin`.

## Notes for the staff

**The store directory and the store count disagree, and that is intentional.**
The directory comes from a 2017 dataset of 28,289 stores. The store count chart
comes from annual reports and reaches 40,990 for FY2025. Both figures are correct
for their own date. The Sources page explains this rather than resolving it
silently.

**Some figures are held in the view rather than the database.** Comparable store
sales are reported inconsistently across quarters, sometimes globally and
sometimes for one region only, so the three verified figures used on the Overview
page are defined in `views.py` rather than modelled. The Sources page flags this.

**External libraries are loaded from CDNs.** Bootstrap and Chart.js are not
Python packages, so `requirements.txt` lists only Django. An internet connection
is needed for styling and charts to appear.