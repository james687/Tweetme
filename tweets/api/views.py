from rest_framework.generics import ListAPIView

from tweets.models import Tweet
from .serializers import TweetModelSerializer


class TweetListAPIView(ListAPIView):
    serializer_class = TweetModelSerializer

    def get_queryset(self):
        return Tweet.objects.all()
