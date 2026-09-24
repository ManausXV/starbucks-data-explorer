from django.shortcuts import render
from .models import FinancialYear, SegmentPerformance, ProductRevenue, GeographyRevenue, StoreCountYear, StoreLocation, MenuDrink, MenuFood, StockQuarter, LoyaltyQuarter
from django.db.models import Count
from django.http import JsonResponse # sending req w/o refreshing

COUNTRY_NAMES = {
    "AE": "United Arab Emirates", "AR": "Argentina", "AT": "Austria", "AW": "Aruba",
    "BE": "Belgium", "BG": "Bulgaria", "BH": "Bahrain", "BN": "Brunei",
    "BS": "Bahamas", "CA": "Canada", "CL": "Chile", "CN": "China",
    "CZ": "Czech Republic", "DE": "Germany", "ES": "Spain", "FR": "France",
    "GB": "United Kingdom", "GR": "Greece", "GT": "Guatemala", "HK": "Hong Kong",
    "HU": "Hungary", "ID": "Indonesia", "IE": "Ireland", "JO": "Jordan",
    "JP": "Japan", "KR": "South Korea", "KW": "Kuwait", "LB": "Lebanon",
    "MO": "Macau", "MX": "Mexico", "MY": "Malaysia", "NL": "Netherlands",
    "NZ": "New Zealand", "OM": "Oman", "PE": "Peru", "PH": "Philippines",
    "PL": "Poland", "PT": "Portugal", "QA": "Qatar", "RO": "Romania",
    "RU": "Russia", "SA": "Saudi Arabia", "SG": "Singapore", "SK": "Slovakia",
    "SV": "El Salvador", "TH": "Thailand", "TR": "Turkey", "TW": "Taiwan",
    "US": "United States",
}
OWNERSHIP_NAMES = {
    "CO": "Company-operated", "LS": "Licensed",
    "JV": "Joint venture", "FR": "Franchise",
}
FILING = "#00704A"
REPORTED = "#B57A22"
DATASET = "#4B5563"

SOURCE_ROWS = [
    {"data": "Total revenue", "source": "Annual reports (10-K)", "tag": "Filing", "color": FILING,
     "coverage": "FY2015 to FY2025", "caveat": "Nothing to flag. It's the top line of the income statement."},
    {"data": "Segment revenue and profit", "source": "FY2025 annual report", "tag": "Filing", "color": FILING,
     "coverage": "FY2023 to FY2025", "caveat": "I leave Corporate & Other out of the charts. It's head office overhead, not a part of the business that sells anything."},
    {"data": "Segment cost lines", "source": "FY2025 annual report", "tag": "Filing", "color": FILING,
     "coverage": "FY2023 to FY2025", "caveat": "Only five cost lines are reported per segment, so the bars don't quite add up to full revenue. More on that below."},
    {"data": "Revenue by product type", "source": "FY2025 annual report", "tag": "Filing", "color": FILING,
     "coverage": "FY2023 to FY2025", "caveat": "Just beverage, food and other. Starbucks doesn't publish anything more detailed."},
    {"data": "Revenue by geography", "source": "FY2025 annual report", "tag": "Filing", "color": FILING,
     "coverage": "FY2023 to FY2025", "caveat": "Only the US and China get their own line. Every other country is lumped together."},
    {"data": "Store counts", "source": "Annual reports (10-K)", "tag": "Filing", "color": FILING,
     "coverage": "FY2012 to FY2025", "caveat": "The split between company-run and licensed stores only appears in three of those years, so I left it out."},
    {"data": "Comparable store sales", "source": "Quarterly results", "tag": "Reported", "color": REPORTED,
     "coverage": "Some quarters", "caveat": "Some quarters report a global figure, others only North America or China. They don't line up into one series, so I only use a few."},
    {"data": "Rewards members", "source": "Quarterly results and news coverage", "tag": "Reported", "color": REPORTED,
     "coverage": "9 readings, FY2020 to FY2026", "caveat": "US only, and it counts people active in the last 90 days. One reading is dated only as \"about 2022\"."},
    {"data": "Share price", "source": "stockanalysis.com", "tag": "Dataset", "color": DATASET,
     "coverage": "Q4 2016 to Q3 2026", "caveat": "Quarterly closing prices. Fine for a long trend, useless for anything day to day."},
    {"data": "Drink nutrition", "source": "Public Kaggle dataset", "tag": "Dataset", "color": DATASET,
     "coverage": "242 drinks", "caveat": "From 2017, so the menu has moved on since. A few teas list caffeine as \"Varies\", which I show as a dash."},
    {"data": "Food nutrition", "source": "Public Kaggle dataset", "tag": "Dataset", "color": DATASET,
     "coverage": "113 items", "caveat": "Also from 2017. There are no categories in this one, which is why the category filter disappears when you switch to food."},
    {"data": "Store locations", "source": "Public Kaggle dataset", "tag": "Dataset", "color": DATASET,
     "coverage": "28,289 stores in 49 countries", "caveat": "From 2017, so a lot of newer stores are missing. Worth reading the note below before trusting the totals."},
]

def index(request):
    segments = SegmentPerformance.objects.filter(fy=2025).exclude(segment="Corporate & Other")
    segment_data = {
        "labels": [s.segment for s in segments],
        "values": [s.net_revenues for s in segments],
    }

    product = ProductRevenue.objects.get(fy=2025)
    product_data = {
        "labels": ["Beverage", "Food", "Other"],
        "values": [product.beverage_pct, product.food_pct, product.other_pct],
    }
    comp_sales_data = {
    "labels": ["FY25 Q1", "FY25 Q4", "FY26 Q1"],
    "values": [-4, 0, 4],
    }

    return render(request, "dashboard/index.html", {
        "segment_data": segment_data,
        "product_data": product_data,
        "comp_sales_data": comp_sales_data
    })

from .models import SegmentPerformance, ProductRevenue, GeographyRevenue

def financials(request):
    years = [2023, 2024, 2025]
    try:
        year = int(request.GET.get("year", 2025))
    except ValueError:
        year = 2025
    if year not in years:
        year = 2025

    revenue_years = FinancialYear.objects.order_by("fy")
    revenue_data = {
        "labels": [f"FY{r.fy}" for r in revenue_years],
        "values": [r.revenue for r in revenue_years],
    }

    segments = SegmentPerformance.objects.filter(fy=year).exclude(segment="Corporate & Other")

    segment_names = ["North America", "International", "Channel Development"]
    margin_datasets = []
    for y in years:
        values = []
        for name in segment_names:
            seg = SegmentPerformance.objects.get(fy=y, segment=name)
            values.append(seg.operating_margin_pct)
        margin_datasets.append({"label": f"FY{y}", "values": values})

    margin_data = {"labels": segment_names, "datasets": margin_datasets}
    cost_fields = [
        ("Product & distribution", "product_costs"),
        ("Store operating", "store_costs"),
        ("Depreciation", "depreciation"),
        ("General & admin", "admin_costs"),
        ("Restructuring", "restructuring"),
        ("Operating income", "operating_income"),
    ]
    expense_datasets = []
    for label, field in cost_fields:
        values = [getattr(seg, field) or 0 for seg in segments]
        expense_datasets.append({"label": label, "values": values})

    expense_data = {
        "labels": [s.segment for s in segments],
        "datasets": expense_datasets,
    }
    geography = GeographyRevenue.objects.get(fy=year)
    geo_data = {
        "labels": ["United States", "China", "Other countries"],
        "values": [geography.usa_pct, geography.china_pct, geography.other_countries_pct],
    }
    return render(request, "dashboard/financials.html", {
        "revenue_data": revenue_data,
        "years": years,
        "year": year,
        "segments": segments,
        "margin_data": margin_data,
        "expense_data": expense_data,
        "geo_data": geo_data,
    })

def stores(request):
    counts = list(StoreCountYear.objects.order_by("fy"))
    first = counts[0]
    previous = counts[-2]
    latest = counts[-1]

    biggest_gain = 0
    biggest_year = None
    for i in range(1, len(counts)):
        gain = counts[i].total - counts[i - 1].total
        if gain > biggest_gain:
            biggest_gain = gain
            biggest_year = counts[i].fy

    count_data = {
        "labels": [f"FY{c.fy}" for c in counts],
        "values": [c.total for c in counts],
    }

    top_countries = (
        StoreLocation.objects
        .values("country_code")
        .annotate(store_count=Count("id"))
        .order_by("-store_count")[:10]
    )

    country_data = {
        "labels": [COUNTRY_NAMES.get(c["country_code"], c["country_code"]) for c in top_countries],
        "values": [c["store_count"] for c in top_countries],
    }

    return render(request, "dashboard/stores.html", {
        "latest": latest,
        "one_year_gain": latest.total - previous.total,
        "first": first,
        "growth": round(latest.total / first.total, 1),
        "biggest_gain": biggest_gain,
        "biggest_year": biggest_year,
        "count_data": count_data,
        "country_data": country_data,
        "total_locations": StoreLocation.objects.count(),
        "country_options": sorted(COUNTRY_NAMES.items(), key=lambda item: item[1]),
        "ownership_options": OWNERSHIP_NAMES.items(),
    })

def store_search(request):
    query = request.GET.get("q", "").strip()
    country = request.GET.get("country", "")
    owner = request.GET.get("owner", "")

    results = StoreLocation.objects.all()
    if query:
        results = results.filter(city__icontains=query)
    if country:
        results = results.filter(country_code=country)
    if owner:
        results = results.filter(ownership_type=owner)

    total = results.count()
    stores = [
        {
            "city": s.city,
            "region": s.subdivision_code,
            "country": COUNTRY_NAMES.get(s.country_code, s.country_code),
            "ownership": OWNERSHIP_NAMES.get(s.ownership_type, s.ownership_type),
            "number": s.store_number,
        }
        for s in results.order_by("city")[:50]
    ]

    return JsonResponse({"total": total, "stores": stores})

def menu(request):
    top_caffeine = MenuDrink.objects.filter(caffeine__isnull=False).order_by("-caffeine").first()
    top_sugar = MenuDrink.objects.filter(sugars__isnull=False).order_by("-sugars").first()
    top_protein = MenuFood.objects.filter(protein__isnull=False).order_by("-protein").first()

    drinks = list(MenuDrink.objects.values(
        "beverage", "category", "prep", "calories", "sugars", "caffeine", "protein"
    ))
    foods = list(MenuFood.objects.values("name", "calories", "fat", "carbs", "protein"))

    return render(request, "dashboard/menu.html", {
        "top_caffeine": top_caffeine,
        "top_sugar": top_sugar,
        "top_protein": top_protein,
        "drinks": drinks,
        "foods": foods,
    })

def stock(request):
    latest = StockQuarter.objects.order_by("-id").first()
    highest = StockQuarter.objects.order_by("-close").first()
    best = StockQuarter.objects.order_by("-change_pct").first()
    worst = StockQuarter.objects.order_by("change_pct").first()

    quarters = list(StockQuarter.objects.order_by("id"))
    price_data = {
        "labels": [q.quarter for q in quarters],
        "values": [q.close for q in quarters],
    }

    change_data = {
        "labels": [q.quarter for q in quarters],
        "values": [q.change_pct for q in quarters],
    }
    loyalty = list(LoyaltyQuarter.objects.order_by("id"))
    loyalty_data = {
        "labels": [l.period for l in loyalty],
        "values": [l.members_millions for l in loyalty],
    }

    return render(request, "dashboard/stock.html", {
        "latest": latest,
        "highest": highest,
        "best": best,
        "worst": worst,
        "price_data": price_data,
        "change_data": change_data,
        "loyalty_data": loyalty_data,
    })

def sources(request):
    return render(request, "dashboard/sources.html", {
        "source_rows": SOURCE_ROWS,
    })