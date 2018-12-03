from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from twitter_clone.models import TwitterUser, Tweet, Notification
from twitter_clone.forms import LoginForm, SignupForm


@login_required
def home_view(request):
    tweets = []
    return render(request, 'home.html', {'user': request.user, 'tweets': tweets})


def login_view(request):
    form = LoginForm(None or request.POST)
    if form.is_valid():
        data = form.cleaned_data
        user = authenticate(
            username=data['username'],
            password=data['password']
            )
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(request.GET.get('next'))
    return render(request, 'login.html', {'form': form})


def signup_view(request):
    form = SignupForm(None or request.POST)
    if form.is_valid():
        data = form.cleaned_data
        user = User.objects.create_user(
            data['username'],
            data['email'],
            data['password'],
            )
        TwitterUser.objects.create(
            user=user,
            username=data['username'],
            handle=''.join(['@', data['handle'].lower().replace(' ', '')]),
        )

        login(request, user)
        return HttpResponseRedirect('/')
    return render(request, 'signup.html', {'form': form, 'user': request.user})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))
