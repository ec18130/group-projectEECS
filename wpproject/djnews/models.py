from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxLengthValidator

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


# Model for holding user data
# 1-1 user relationship
# DOB
# Picture
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    dob = models.DateField(default="1000-01-01")
    # image = models.ImageField(upload_to='images')

    def __str__(self):
        string = 'user: ' + str(self.user) + '\n'
        string += 'dob: ' + str(self.dob) + '\n'
        return string

