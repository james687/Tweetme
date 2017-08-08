from django.conf.urls import url

from .views import TweetList, TweetDetail

urlpatterns = [
    url(r'^$', TweetList.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', TweetDetail.as_view(), name='detail')
]