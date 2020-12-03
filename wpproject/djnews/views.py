from datetime import datetime, date
from smtplib import SMTPException

from django.contrib.auth import login
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from djnews.forms import CustomUserCreationForm, ProfileForm
from djnews.models import Profile, NewsArticle, NewsCategory


class ProfileView(View):
    template_name = "djnews/profile.html"

    @staticmethod
    def get(request):
        p = Profile.objects.get(user=request.user)
        if date(1000, 1, 1) == p.dob:
            p.dob = None
        context = {'user': request.user, 'profile': p}
        return render(request, "djnews/profile.html", context=context)


class LandingView(TemplateView):
    template_name = "djnews/landing.html"


class RegisterView(View):
    @staticmethod
    def get(request):
        return render(
            request, "djnews/register.html",
            {"form": CustomUserCreationForm}
        )

    # TODO: prevent users with the same email
    @staticmethod
    def post(request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            try:
                send_mail(
                    'Welcome!',
                    'Thank you for joining DJNews!',
                    'ecs639uprojectsuperuser@gmail.com',
                    [user.email],
                    fail_silently=False,
                )
            except SMTPException as e:
                print('Error sending email')
            finally:
                return redirect(reverse("landing"))
        else:
            return render(request, 'djnews/register.html', {'form': form})


class GetProfileDetails(View):
    @staticmethod
    def post(request):
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = Profile.objects.get(user=request.user)
            profile.dob = form.cleaned_data.get("dob")
            profile.save()
            return redirect('profile')
        return render(request, 'djnews/profile_form.html', {'form': form})

    @staticmethod
    def get(request):
        form = ProfileForm()
        return render(request, 'djnews/profile_form.html', {'form': form})


def is_valid_queryparam(param):
    return param != '' and param is not None


def index(request):
    queryset = NewsArticle.objects.all()
    categories = NewsCategory.objects.all()
    category = request.GET.get('category')

    if is_valid_queryparam(category) and category != 'All':
        queryset = queryset.filter(category__name=category)

    context = {
        "articles": queryset,
        "categories": categories,
    }
    return render(request, "djnews/landing.html", context)
