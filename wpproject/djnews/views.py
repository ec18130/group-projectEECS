from django.views.generic import TemplateView


# @login_required
class ProfileView(TemplateView):
    template_name = "djnews/profile.html"


class LandingView(TemplateView):
    template_name = "djnews/landing.html"
