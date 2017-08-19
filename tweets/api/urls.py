from django.conf.urls import url

from .views import TweetListAPIView, TweetCreateAPIView

urlpatterns = [
    url(r'^$', TweetListAPIView.as_view(), name='list'),
    url(r'^create/$', TweetCreateAPIView.as_view(), name='create'),
]