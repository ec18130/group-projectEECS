from django.urls import path

from djnews.views import *

urlpatterns = [
    path('profile/', ProfileView.as_view()),
]
