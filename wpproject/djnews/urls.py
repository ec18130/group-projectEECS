from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.contrib.auth import views as auth_views
from djnews.views import *

urlpatterns = [
    path('accounts/', include("django.contrib.auth.urls")),
    path('profile/', login_required(ProfileView.as_view()), name="profile"),
    path('register/', RegisterView.as_view(), name="register"),
    path('', login_required(index), name="index"),
    ##path('', login_required(LandingView.as_view()), name="landing"),
]
