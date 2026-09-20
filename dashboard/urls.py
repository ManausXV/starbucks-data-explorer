from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("financials", views.financials, name="financials"),
]