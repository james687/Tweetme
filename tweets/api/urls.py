from django.conf.urls import url

from .views import TweetListAPIView

urlpatterns = [
    url(r'^$', TweetListAPIView.as_view(), name='list')
]