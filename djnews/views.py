from collections import deque
from datetime import datetime, date
from queue import Queue
from smtplib import SMTPException

from django.contrib.auth import login
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
import json

from djnews.forms import CustomUserCreationForm, ProfileForm
from djnews.models import Profile, NewsArticle, NewsCategory, Comment


# Class for viewing profile page
class ProfileView(View):
    template_name = "djnews/profile.html"

    @staticmethod
    def get(request, profile_id):
        p = get_object_or_404(Profile, pk=profile_id)
        if date(1000, 1, 1) == p.dob:
            p.dob = None
        context = {'user': request.user, 'profile': p}
        return render(request, "djnews/profile.html", context=context)


# TODO: think this can be removed but cba to check rn
class LandingView(TemplateView):
    template_name = "djnews/landing.html"


# Class for handling registration page
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


# Class for handling editing profile details
class GetProfileDetails(View):
    @staticmethod
    def get(request):
        form = ProfileForm()
        return render(request, 'djnews/profile_form.html', {'form': form})

    @staticmethod
    def post(request):
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = Profile.objects.get(user=request.user)
            profile.dob = form.cleaned_data.get("dob")
            profile.save()
            return redirect('profile')
        return render(request, 'djnews/profile_form.html', {'form': form})


# Landing page function
def index(request):
    # Query validation
    def is_valid_queryparam(param):
        return param != '' and param is not None

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


class CommentsView(View):
    @staticmethod
    def get(request, article_id):
        # recursive function for construction of JSON tree structure of comments
        def recursive_add_child_comment(parent, child_comment_data):
            child_comments = Comment.objects.filter(article=article, parent=parent)
            for child_comment in child_comments:
                child_comment_data.append({
                    'id': child_comment.id,
                    'author': serialise_user(child_comment.author),
                    'dateCreated': child_comment.dateCreated,
                    'dateUpdated': child_comment.dateUpdated,
                    'text': child_comment.text,
                    'parent': parent.id,
                    'children': recursive_add_child_comment(child_comment, []),
                    'article': article.id,
                })
            return child_comment_data

        # get article and top level comments
        article = get_object_or_404(NewsArticle, pk=article_id)
        top_level_comments = Comment.objects.filter(article=article, parent=None)

        if top_level_comments:
            count = 0
            comments_serialised_data = []

            # create top level of JSON tree and then recursively explore each branch
            for top_level_comment in top_level_comments:
                comments_serialised_data.append({
                    'id': top_level_comment.id,
                    'author': serialise_user(top_level_comment.author),
                    'dateCreated': top_level_comment.dateCreated,
                    'dateUpdated': top_level_comment.dateUpdated,
                    'text': top_level_comment.text,
                    'parent': None,
                    'children': recursive_add_child_comment(top_level_comment, []),
                    'article': article.id,
                })
                count += 1

            data = {
                'comments': comments_serialised_data
            }
            return JsonResponse(data)
        else:
            return JsonResponse({"message": "No comments found"}, status=200)

    @staticmethod
    def post(request, article_id):
        try:
            body = json.loads(request.body)
            comment = Comment(
                author=request.user,
                text=body.get('text'),
                article=NewsArticle.objects.get(pk=article_id),
                parent= Comment.objects.get(pk=body.get('parent')),
            )
            comment.save()
            return JsonResponse({"message": "Comment added"}, status=200)
        except TypeError as ex:
            print(ex)
            return JsonResponse({"message": "Comment not added"}, status=400)

    @staticmethod
    def delete(request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.delete()
        return JsonResponse({"message": "comment deleted"})

    @staticmethod
    def put(request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        body = json.loads(request.body)
        comment.text = body.get('text')
        comment.save()
        return JsonResponse({"message": "comment edited"})



# function to serialise user object
def serialise_user(user):
    return {
        'id': user.id,
        'username': user.username
    }
