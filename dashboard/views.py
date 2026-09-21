from django.shortcuts import render
from .models import FinancialYear, SegmentPerformance, ProductRevenue, GeographyRevenue

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

