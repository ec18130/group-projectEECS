from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from djnews.forms import CustomUserCreationForm


class ProfileView(TemplateView):
    template_name = "djnews/profile.html"


class LandingView(TemplateView):
    template_name = "djnews/landing.html"


class RegisterView(View):
    def get(self, request):
        return render(
            request, "djnews/register.html",
            {"form": CustomUserCreationForm}
        )

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("landing"))
