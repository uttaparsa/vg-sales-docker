from django.urls import path

from analysis.views import SalesComparisonByGame, TotalSalesByYearsPeriod, CategorySalesByYear, \
    PublishersSalesComparisonByYearsPeriod

urlpatterns = [
    path('publishers-sales-comparison-by-years-period/', PublishersSalesComparisonByYearsPeriod.as_view()),
    path('sales-comparison-by-game/', SalesComparisonByGame.as_view()),
    path('sales-by-year-period/', TotalSalesByYearsPeriod.as_view()),
    path('category-sales-by-year-period/', CategorySalesByYear.as_view()),
]

