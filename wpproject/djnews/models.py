from django.contrib.auth.models import User
from django.db import models


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
