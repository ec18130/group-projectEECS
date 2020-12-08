from datetime import datetime

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("User with that email already exists.")
        return self.cleaned_data


class ProfileForm(forms.Form):
    cur_year = datetime.today().year
    year_range = tuple([i for i in range(cur_year - 100, cur_year + 1)])
    dob = forms.DateField(label='Date of Birth', widget=forms.SelectDateWidget(years=year_range))
