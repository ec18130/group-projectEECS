from smtplib import SMTPException

from django.contrib.auth import login
from django.core.mail import send_mail
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

    # TODO: prevent users with the same email
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
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
