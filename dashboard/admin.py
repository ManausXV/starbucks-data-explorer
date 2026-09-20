from django.contrib import admin

# Register your models here.
from dashboard.models import (
    FinancialYear, SegmentPerformance, ProductRevenue, GeographyRevenue,
    StoreCountYear, StockQuarter, LoyaltyQuarter, MenuDrink, MenuFood, StoreLocation
)
admin.site.register(FinancialYear)
admin.site.register(SegmentPerformance)
admin.site.register(ProductRevenue)
admin.site.register(GeographyRevenue)
admin.site.register(StoreCountYear)
admin.site.register(StockQuarter)
admin.site.register(LoyaltyQuarter)
admin.site.register(MenuDrink)
admin.site.register(MenuFood)
admin.site.register(StoreLocation)