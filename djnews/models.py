from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxLengthValidator


# Model for category types of articles
class NewsCategory(models.Model):
    name = models.CharField(max_length=124)

    def __str__(self):
        return self.name


# Model for news articles
class NewsArticle(models.Model):
    title = models.CharField(max_length=1000)
    category = models.ForeignKey(NewsCategory, null=True, on_delete=models.SET_NULL)
    date = models.DateField(blank=False)
    author = models.CharField(max_length=124)
    article = models.TextField()
    likes = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.title


# Model for holding user data
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    dob = models.DateField(default="1000-01-01")

    # image = models.ImageField(upload_to='images')

    def __str__(self):
        string = 'user: ' + str(self.user) + '\n'
        string += 'dob: ' + str(self.dob) + '\n'
        return string


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=350)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        string = 'id: ' + str(self.id) + '\n'
        string += 'author: ' + str(self.author) + '\n'
        string += 'dateCreated: ' + str(self.dateCreated) + '\n'
        string += 'dateUpdated: ' + str(self.dateUpdated) + '\n'
        string += 'text: ' + str(self.text) + '\n'
        if self.parent is None:
            string += 'parent: None'
        else:
            string += 'parent: ' + str(self.parent.id) + '\n'
        return string
