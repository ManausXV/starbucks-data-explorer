import csv
import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from dashboard.models import (
    FinancialYear, SegmentPerformance, ProductRevenue, GeographyRevenue,
    StoreCountYear, StockQuarter, LoyaltyQuarter, MenuDrink, MenuFood, StoreLocation
)

DATA_DIR = os.path.join(settings.BASE_DIR, 'dashboard', 'data')


def safe_float(value):
    """Convert a value to float, or None if it's missing/non-numeric (e.g. 'Varies')."""
    if value is None or value == '':
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


class Command(BaseCommand):
    help = "Loads Starbucks data from the JSON and CSV files into the database."

    def handle(self, *args, **options):
        with open(os.path.join(DATA_DIR, 'starbucks_data_v3.json'), encoding='utf-8') as f:
            data = json.load(f)

        self.load_financial_years(data)
        self.load_segment_performance(data)
        self.load_product_revenue(data)
        self.load_geography_revenue(data)
        self.load_store_counts(data)
        self.load_stock_quarters(data)
        self.load_loyalty_quarters(data)
        self.load_menu_drinks()
        self.load_menu_food()
        self.load_store_locations()

        self.stdout.write(self.style.SUCCESS("All data loaded successfully."))

    def load_financial_years(self, data):
        FinancialYear.objects.all().delete()
        for row in data['revenue_annual']['series']:
            FinancialYear.objects.create(fy=row['fy'], revenue=row['revenue'])
        self.stdout.write(f"Loaded {FinancialYear.objects.count()} FinancialYear rows.")

    def load_segment_performance(self, data):
        SegmentPerformance.objects.all().delete()
        segment_labels = {
            'north_america': 'North America',
            'international': 'International',
            'channel_development': 'Channel Development',
            'corporate_and_other': 'Corporate & Other',
        }
        for year_key, year_data in data['segment_pl'].items():
            if not year_key.startswith('fiscal_'):
                continue
            fy = int(year_key.replace('fiscal_', ''))
            for seg_key, label in segment_labels.items():
                seg = year_data.get(seg_key)
                if not seg:
                    continue
                SegmentPerformance.objects.create(
                    fy=fy,
                    segment=label,
                    net_revenues=seg.get('net_revenues'),
                    operating_income=seg.get('operating_income'),
                    operating_margin_pct=seg.get('operating_margin_pct'),
                )
        self.stdout.write(f"Loaded {SegmentPerformance.objects.count()} SegmentPerformance rows.")

    def load_product_revenue(self, data):
        ProductRevenue.objects.all().delete()
        for row in data['revenue_by_product_type']['series']:
            ProductRevenue.objects.create(
                fy=row['fy'],
                beverage=row['beverage'], beverage_pct=row['beverage_pct'],
                food=row['food'], food_pct=row['food_pct'],
                other=row['other'], other_pct=row['other_pct'],
                total=row['total'],
            )
        self.stdout.write(f"Loaded {ProductRevenue.objects.count()} ProductRevenue rows.")

    def load_geography_revenue(self, data):
        GeographyRevenue.objects.all().delete()
        for row in data['revenue_by_geography']['series']:
            total = row['total']
            usa, china, other = row['united_states'], row['china'], row['other_countries']
            GeographyRevenue.objects.create(
                fy=row['fy'],
                usa=usa, usa_pct=round(usa / total * 100, 1),
                china=china, china_pct=round(china / total * 100, 1),
                other_countries=other, other_countries_pct=round(other / total * 100, 1),
                total=total,
            )
        self.stdout.write(f"Loaded {GeographyRevenue.objects.count()} GeographyRevenue rows.")

    def load_store_counts(self, data):
        StoreCountYear.objects.all().delete()
        for row in data['store_counts']['annual_series']:
            StoreCountYear.objects.create(
                fy=row['fy'],
                total=row['total'],
                company_operated=row.get('company_operated'),
                licensed=row.get('licensed'),
            )
        self.stdout.write(f"Loaded {StoreCountYear.objects.count()} StoreCountYear rows.")

    def load_stock_quarters(self, data):
        StockQuarter.objects.all().delete()
        for quarter, open_p, high, low, close, change_pct, volume in data['stock_price_real']['series']:
            StockQuarter.objects.create(
                quarter=quarter, open_price=open_p, high=high, low=low,
                close=close, change_pct=change_pct, volume=volume,
            )
        self.stdout.write(f"Loaded {StockQuarter.objects.count()} StockQuarter rows.")

    def load_loyalty_quarters(self, data):
        LoyaltyQuarter.objects.all().delete()
        for row in data['loyalty_program']['series']:
            LoyaltyQuarter.objects.create(period=row['period'], members_millions=row['members_millions'])
        self.stdout.write(f"Loaded {LoyaltyQuarter.objects.count()} LoyaltyQuarter rows.")

    def load_menu_drinks(self):
        MenuDrink.objects.all().delete()
        path = os.path.join(DATA_DIR, 'starbucks_drinkMenu_expanded.csv')
        with open(path, encoding='utf-8') as f:
            for row in csv.DictReader(f):
                MenuDrink.objects.create(
                    category=row['Beverage_category'].strip(),
                    beverage=row['Beverage'].strip(),
                    prep=row['Beverage_prep'].strip(),
                    calories=safe_float(row['Calories']),
                    total_fat=safe_float(row[' Total Fat (g)']),
                    sodium=safe_float(row[' Sodium (mg)']),
                    total_carbs=safe_float(row[' Total Carbohydrates (g) ']),
                    sugars=safe_float(row[' Sugars (g)']),
                    protein=safe_float(row[' Protein (g) ']),
                    caffeine=safe_float(row['Caffeine (mg)']),
                )
        self.stdout.write(f"Loaded {MenuDrink.objects.count()} MenuDrink rows.")

    def load_menu_food(self):
        MenuFood.objects.all().delete()
        path = os.path.join(DATA_DIR, 'starbucks-menu-nutrition-food.csv')
        with open(path, encoding='utf-16') as f:
            for row in csv.DictReader(f):
                MenuFood.objects.create(
                    name=row[''].strip(),
                    calories=safe_float(row[' Calories']),
                    fat=safe_float(row[' Fat (g)']),
                    carbs=safe_float(row[' Carb. (g)']),
                    fiber=safe_float(row[' Fiber (g)']),
                    protein=safe_float(row[' Protein (g)']),
                )
        self.stdout.write(f"Loaded {MenuFood.objects.count()} MenuFood rows.")

    def load_store_locations(self):
        StoreLocation.objects.all().delete()
        path = os.path.join(DATA_DIR, 'startbucks.csv')
        stores = []
        with open(path, encoding='utf-8') as f:
            for row in csv.DictReader(f):
                stores.append(StoreLocation(
                    store_number=row['storeNumber'],
                    country_code=row['countryCode'],
                    ownership_type=row['ownershipTypeCode'],
                    city=row['city'],
                    subdivision_code=row['countrySubdivisionCode'],
                    latitude=safe_float(row['latitude']),
                    longitude=safe_float(row['longitude']),
                ))
        StoreLocation.objects.bulk_create(stores, batch_size=500)
        self.stdout.write(f"Loaded {StoreLocation.objects.count()} StoreLocation rows.")