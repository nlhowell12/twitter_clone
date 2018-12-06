import re

from django import template

from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from twitter_clone.models import TwitterUser, Tweet, Notification
from twitter_clone.forms import LoginForm, SignupForm, NewTweetForm

register = template.Library()


def get_twitter_user(request):
    user = TwitterUser.objects.filter(username=request.user.username).first()
    return user


@login_required
def home_view(request):
    user = get_twitter_user(request)
    tweets = list(Tweet.objects.filter(user=user))
    user_tweet_count = Tweet.objects.filter(user=user).count
    for other_user in user.following.all():
        other_tweets = list(Tweet.objects.filter(user=other_user))
        tweets = tweets + other_tweets
    notifications = Notification.objects.filter(user=user)
    return render(
        request,
        'home.html',
        ({
            'user': user,
            'tweets': tweets,
            'notification_count': len(notifications),
            'user_tweet_count': user_tweet_count,
            'logged_in': request.user.is_authenticated
            })
        )


def profile_card_view(request):
    return render(
        request,
        'profilecard.html',
        {'user': request.user}
    )


def new_tweet_view(request):
    twitter_user = get_twitter_user(request)
    form = NewTweetForm(None or request.POST)
    if form.is_valid():
        data = form.cleaned_data
        tweet = Tweet.objects.create(
            user=TwitterUser.objects.filter(
                username=request.user.username).first(),
            body=data['tweet']
        )
        if '@' in data['tweet']:
            users = re.findall(r'[@]\w+', data['tweet'])
            for user in users:
                Notification.objects.create(
                    user=TwitterUser.objects.filter(handle=user).first(),
                    tweet=tweet,
                )
        return HttpResponseRedirect(reverse('homepage'))
    return render(
        request, 'newtweet.html', {'form': form, 'user': twitter_user})


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


def notification_view(request):
    user = get_twitter_user(request)
    db_notifications = Notification.objects.filter(
        user=user
        )
    notifications = list(db_notifications)
    user_tweet_count = Tweet.objects.filter(user=user).count
    for notification in db_notifications:
        notification.delete()
    return render(
        request,
        'notifications.html',
        {
            'user': user,
            'notifications': notifications,
            'notification_count': len(notifications),
            'user_tweet_count': user_tweet_count
            })


def profile_view(request, id):
    user = TwitterUser.objects.filter(id=id).first()
    current_user = {}
    following = []
    notifications = []
    if not request.user.is_anonymous:
        current_user = TwitterUser.objects.filter(
            id=request.user.twitteruser.id).first()
        following = list(current_user.following.all())
        notifications = Notification.objects.filter(user=current_user)
    tweets = Tweet.objects.filter(user=user)
    user_tweet_count = Tweet.objects.filter(user=user).count
    return render(
        request,
        'profile.html',
        {
            'user': user,
            'tweets': tweets,
            'notification_count': len(notifications),
            'current_user': current_user,
            'user_tweet_count': user_tweet_count,
            'following': following,
            'logged_in': request.user.is_authenticated
        }
    )


def follow(request, id):
    user = TwitterUser.objects.filter(id=id).first()
    current_user = TwitterUser.objects.filter(
        id=request.user.twitteruser.id).first()
    if user in current_user.following.all():
        current_user.following.remove(user)
    else:
        current_user.following.add(user)
    return HttpResponseRedirect('/profile/{}'.format(id))


def tweet_view(request, id):
    user = get_twitter_user(request) or request.user
    tweet = (Tweet.objects.filter(id=id).first() or {
        'body': 'There is no tweet with that ID'})
    notification_count = 0
    user_tweet_count = 0
    if not request.user.is_anonymous:
        notification_count = Notification.objects.filter(user=user).count
        user_tweet_count = Tweet.objects.filter(user=user).count
    return render(request, 'tweet.html'.format(id), {
        'tweet': tweet,
        'user': user,
        'notification_count': notification_count,
        'user_tweet_count': user_tweet_count,
        'logged_in': request.user.is_authenticated
    })
