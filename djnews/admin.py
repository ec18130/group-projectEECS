from django.contrib import admin

from .models import Profile, NewsCategory, NewsArticle,Comment

admin.site.register(Profile)
admin.site.register(NewsCategory)
admin.site.register(NewsArticle)
admin.site.register(Comment)
