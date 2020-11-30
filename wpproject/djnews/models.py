from django.db import models
from django.core.validators import MaxLengthValidator

# Create your models here.
class NewsCategory(models.Model):
    name = models.CharField(max_length=124)

    def __str__(self):
        return self.name


class NewsArticle(models.Model):
    title = models.CharField(max_length=1000)
    category = models.ForeignKey(NewsCategory, null=True, on_delete= models.SET_NULL)
    date = models.DateField(blank=False)
    author = models.CharField(max_length=124)
    article = models.TextField()

    def __str__(self):
        return self.title