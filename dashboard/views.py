from django.shortcuts import render
from .models import SegmentPerformance

from .models import SegmentPerformance, ProductRevenue

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
    segments = SegmentPerformance.objects.filter(fy=2025).exclude(segment="Corporate & Other")
    product = ProductRevenue.objects.get(fy=2025)
    geography = GeographyRevenue.objects.get(fy=2025)

    product_mix_data = {
        "labels": ["Beverage", "Food", "Other"],
        "values": [product.beverage_pct, product.food_pct, product.other_pct],
    }

    geo_mix_data = {
        "labels": ["United States", "China", "Other Countries"],
        "values": [geography.usa_pct, geography.china_pct, geography.other_countries_pct],
    }

    return render(request, "dashboard/financials.html", {
        "segments": segments,
        "product": product,
        "geography": geography,
        "product_mix_data": product_mix_data,
        "geo_mix_data": geo_mix_data,
    })