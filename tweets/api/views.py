from pprint import pprint

from django.db.models import Q
from rest_framework import permissions
from rest_framework.generics import ListAPIView, CreateAPIView

from tweets.models import Tweet
from .serializers import TweetModelSerializer


class TweetListAPIView(ListAPIView):
    serializer_class = TweetModelSerializer

    def get_queryset(self):
        qs = Tweet.objects.all()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(Q(content__icontains=query) | Q(user__username__icontains=query))
        return qs


class TweetCreateAPIView(CreateAPIView):
    serializer_class = TweetModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        pprint(vars(serializer))
        serializer.save(user=self.request.user)
