from django.urls import path

from .views import Profile, SignUpUser




urlpatterns = [
    path('profile/', Profile.as_view()),

    path('signup/', SignUpUser.as_view()),
]

