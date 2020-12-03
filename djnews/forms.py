from datetime import datetime

from django.contrib.auth.forms import UserCreationForm
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)


class ProfileForm(forms.Form):
    cur_year = datetime.today().year
    year_range = tuple([i for i in range(cur_year - 100, cur_year + 1)])
    dob = forms.DateField(label='Date of Birth', widget=forms.SelectDateWidget(years=year_range))
