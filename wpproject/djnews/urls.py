from django.urls import path, include
from djnews.views import *

urlpatterns = [
    path('accounts/', include("django.contrib.auth.urls")),
    path('profile/', ProfileView.as_view()),
    path('landing/', LandingView.as_view()),
]
