from django.urls import path

from .views import RankView, NameView, FiveBestSellersBasedOnYearAndPlatform, AmericanSellsMoreThanBritish

urlpatterns = [
    path('rank/<int:rank>/', RankView.as_view()),
    path('name/', NameView.as_view()),
    path('five-best-sellers/', FiveBestSellersBasedOnYearAndPlatform.as_view()),
    path('american-sells-more-than-european/', AmericanSellsMoreThanBritish.as_view()),
]

