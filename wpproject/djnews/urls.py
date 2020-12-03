from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.contrib.auth import views as auth_views
from djnews.views import *

urlpatterns = [
    path('comments/<int:article_id>/', login_required(CommentsView.as_view()), name="comments"),
    path('comments/edit/<int:comment_id>/', login_required(CommentsView.as_view()), name="comments"),
    path('accounts/', include("django.contrib.auth.urls")),
    path('profile/details/', login_required(GetProfileDetails.as_view()), name="profile-details"),
    path('profile/<int:profile_id>/', login_required(ProfileView.as_view()), name="profile"),
    path('register/', RegisterView.as_view(), name="register"),
    path('', login_required(index), name="index"),
    #path('', login_required(LandingView.as_view()), name="landing"),
]
