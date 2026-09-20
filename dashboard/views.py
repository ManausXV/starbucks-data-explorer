from django.shortcuts import render
from .models import SegmentPerformance

def index(request):
    segments = SegmentPerformance.objects.filter(fy=2025).exclude(segment="Corporate & Other")
    segment_data = {
        "labels": [s.segment for s in segments],
        "values": [s.net_revenues for s in segments],
    }
    return render(request, "dashboard/index.html", {
        "segment_data": segment_data,
    })
