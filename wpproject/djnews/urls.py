from django.contrib.auth.decorators import login_required
from django.urls import path, include
from djnews.views import *

urlpatterns = [
    path('accounts/', include("django.contrib.auth.urls")),
    path('profile/', login_required(ProfileView.as_view())),
    path('landing/', login_required(LandingView.as_view())),
]
