from django.db import models

# Models for Starbucks Data Explorer
class FinancialYear(models.Model):
    fy = models.IntegerField(unique=True)
    revenue = models.FloatField()

    def __str__(self):
        return f"FY{self.fy}: ${self.revenue}B"


class SegmentPerformance(models.Model):
    fy = models.IntegerField()
    segment = models.CharField(max_length=30)
    net_revenues = models.FloatField()
    operating_income = models.FloatField(null=True, blank=True)
    operating_margin_pct = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"FY{self.fy} — {self.segment}"


class ProductRevenue(models.Model):
    fy = models.IntegerField(unique=True)
    beverage = models.FloatField()
    beverage_pct = models.FloatField()
    food = models.FloatField()
    food_pct = models.FloatField()
    other = models.FloatField()
    other_pct = models.FloatField()
    total = models.FloatField()

    def __str__(self):
        return f"FY{self.fy} product revenue"


class GeographyRevenue(models.Model):
    fy = models.IntegerField(unique=True)
    usa = models.FloatField()
    usa_pct = models.FloatField()
    china = models.FloatField()
    china_pct = models.FloatField()
    other_countries = models.FloatField()
    other_countries_pct = models.FloatField()
    total = models.FloatField()

    def __str__(self):
        return f"FY{self.fy} geography revenue"


class StoreCountYear(models.Model):
    fy = models.IntegerField(unique=True)
    total = models.IntegerField()
    company_operated = models.IntegerField(null=True, blank=True)
    licensed = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"FY{self.fy}: {self.total} stores"

2
class StockQuarter(models.Model):
    quarter = models.CharField(max_length=20)
    open_price = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    change_pct = models.FloatField()
    volume = models.BigIntegerField()

    def __str__(self):
        return f"{self.quarter}: ${self.close}"


class LoyaltyQuarter(models.Model):
    period = models.CharField(max_length=20)
    members_millions = models.FloatField()

    def __str__(self):
        return f"{self.period}: {self.members_millions}M members"

class MenuDrink(models.Model):
    category = models.CharField(max_length=100)
    beverage = models.CharField(max_length=150)
    prep = models.CharField(max_length=50, blank=True)
    calories = models.FloatField(null=True, blank=True)
    total_fat = models.FloatField(null=True, blank=True)
    sodium = models.FloatField(null=True, blank=True)
    total_carbs = models.FloatField(null=True, blank=True)
    sugars = models.FloatField(null=True, blank=True)
    protein = models.FloatField(null=True, blank=True)
    caffeine = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.beverage} ({self.prep})"


class MenuFood(models.Model):
    name = models.CharField(max_length=150)
    calories = models.FloatField(null=True, blank=True)
    fat = models.FloatField(null=True, blank=True)
    carbs = models.FloatField(null=True, blank=True)
    fiber = models.FloatField(null=True, blank=True)
    protein = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class StoreLocation(models.Model):
    store_number = models.CharField(max_length=50)
    country_code = models.CharField(max_length=10)
    ownership_type = models.CharField(max_length=10)
    city = models.CharField(max_length=100, blank=True)
    subdivision_code = models.CharField(max_length=20, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.store_number} ({self.city})"
    