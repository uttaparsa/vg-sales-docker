from django.urls import path

from analysis.views import SalesComparisonByGame, SalesByYearsPeriod, CategorySalesByYear

urlpatterns = [
    path('sales-comparison-by-game/', SalesComparisonByGame.as_view()),
    path('sales-by-year-period/', SalesByYearsPeriod.as_view()),
    path('category-sales-by-year-period/', CategorySalesByYear.as_view()),
]

