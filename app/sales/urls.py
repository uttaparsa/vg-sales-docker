from django.urls import path

from sales.views import RankView, NameView, FiveBestSellersBasedOnYearAndPlatform, AmericanSellsMoreThanBritish, \
    SalesComparisonByGame, SalesByYearsPeriod, CategorySalesByYear

urlpatterns = [
    path('rank/<int:rank>/', RankView.as_view()),
    path('name/', NameView.as_view()),
    path('five-best-sellers/', FiveBestSellersBasedOnYearAndPlatform.as_view()),
    path('american-sells-more-than-european/', AmericanSellsMoreThanBritish.as_view()),
    path('sales-comparison-by-game/', SalesComparisonByGame.as_view()),
    path('sales-by-year-period/', SalesByYearsPeriod.as_view()),
    path('category-sales-by-year-period/', CategorySalesByYear.as_view()),
]

