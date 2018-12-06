"""twitter_clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path

from twitter_clone.models import TwitterUser, Tweet, Notification
from twitter_clone.views import (
    home_view, login_view, signup_view,
    logout_view, new_tweet_view, notification_view, profile_view, follow,
    tweet_view
    )

admin.site.register(TwitterUser)
admin.site.register(Tweet)
admin.site.register(Notification)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notifications/', notification_view),
    path('', home_view, name='homepage'),
    path('profile/<int:id>', profile_view),
    path('login/', login_view),
    path('signup/', signup_view),
    path('logout/', logout_view),
    path('newtweet/', new_tweet_view),
    path('follow/<int:id>', follow),
    path('tweet/<int:id>', tweet_view)
]
