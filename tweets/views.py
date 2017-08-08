from django.shortcuts import render

from .models import Tweet

def tweet_detail_view(request, id):
    context = {
        'object': Tweet.objects.get(id=id)
    }
    return render(request, 'detail_view.html', context)

def tweet_list_view(request):
    context = {
        'object_list': Tweet.objects.all()
    }
    return render(request, 'list_view.html', context)