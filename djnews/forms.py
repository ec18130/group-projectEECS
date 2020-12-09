from datetime import datetime

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("User with that email already exists.")
        return self.cleaned_data


class ProfileForm(forms.ModelForm):
     class Meta:
        model = Profile
        fields = ['dob', 'image']
        forms.DateInput.input_type='date'
        widgets={
            'dob' : forms.DateInput(attrs={'class' : 'form-control', 'name' : 'dob', 'id' : 'dob', 'value' : '{{ user_id.dob }}'}),
            'image': forms.FileInput(attrs={'class' : 'form-control', 'name' : 'image', 'id' : 'image', 'label': 'Update your profile photo'}),
        }
        labels = {
        'dob': "Date of Birth",
        'image' : "Import Profile Image"
    }
