from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("financials", views.financials, name="financials"),
    path("stores", views.stores, name="stores"),
    path("api/stores", views.store_search, name="store_search"),
    path("menu", views.menu, name="menu"),
    path("stock", views.stock, name="stock"),
    path("sources", views.sources, name="sources"),
]