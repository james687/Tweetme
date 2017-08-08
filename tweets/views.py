from django.views.generic import ListView, DetailView

from .models import Tweet


class TweetList(ListView):
    model = Tweet
    template_name = "list.html"


class TweetDetail(DetailView):
    model = Tweet
    template_name = "detail.html"


# function-based views of list and detail views

# def tweet_detail_view(request, id):
#     context = {
#         'object': Tweet.objects.get(id=id)
#     }
#     return render(request, 'detail.html', context)
#
# def tweet_list_view(request):
#     context = {
#         'object_list': Tweet.objects.all()
#     }
#     return render(request, 'list.html', context)
