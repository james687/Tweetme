from django.conf.urls import url
from django.views.generic import RedirectView

from .views import TweetListSkeleton, TweetDetail, TweetCreate, TweetUpdate, TweetDelete

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/')),
    url(r'^search/$', TweetListSkeleton.as_view(), name='search'),
    url(r'^(?P<pk>\d+)/$', TweetDetail.as_view(), name='detail'),
    url(r'create/', TweetCreate.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/edit/$', TweetUpdate.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/$', TweetDelete.as_view(), name='delete'),
]