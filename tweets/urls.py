from django.conf.urls import url

from .views import TweetList, TweetDetail, TweetCreate

urlpatterns = [
    url(r'^$', TweetList.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', TweetDetail.as_view(), name='detail'),
    url(r'create/', TweetCreate.as_view(), name='create')
]