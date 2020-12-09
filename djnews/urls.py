from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.contrib.auth import views as auth_views
from djnews.views import *

urlpatterns = [
    path('articles/<str:article_filter>/', login_required(get_filtered_articles), name="filtered_articles"),
    path('articles/', login_required(get_articles), name="articles"),
    path('likes/<int:article_id>/', login_required(LikesView.as_view()), name="likes"),
    path('comments/<int:article_id>/', login_required(CommentsView.as_view()), name="comments"),
    path('comments/edit/<int:comment_id>/', login_required(CommentsView.as_view()), name="comments"),
    path('accounts/', include("django.contrib.auth.urls")),
    path('profile/', login_required(ProfileView.as_view()), name="profile"),
    path('profile/details/<str:username>/', login_required(GetProfileDetails.as_view()), name="profile_details"),
    path('profile/<str:username>/', login_required(delete_image), name="delete_Image"),
    path('register/', RegisterView.as_view(), name="register"),
    path('', login_required(index), name="index"),
]