from django.contrib import admin
from .models import NewsCategory
from .models import NewsArticle

# Register your models here.
admin.site.register(NewsCategory)
admin.site.register(NewsArticle)