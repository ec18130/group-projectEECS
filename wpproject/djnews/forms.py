from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)