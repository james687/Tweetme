from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .mixins import FormUserNeededMixin, UserOwnerMixin
from .forms import TweetModelForm
from .models import Tweet


class TweetList(ListView):
    model = Tweet
    template_name = "list.html"


class TweetDetail(DetailView):
    model = Tweet
    template_name = "detail.html"


class TweetCreate(FormUserNeededMixin, CreateView):
    form_class = TweetModelForm
    # if don't use form_class
    # model = Tweet
    # fields = [
    #     'content'
    # ]

    template_name = "create.html"


class TweetUpdate(LoginRequiredMixin, UserOwnerMixin, UpdateView):
    model = Tweet
    form_class = TweetModelForm
    template_name = "update.html"
    login_url = '/admin/'


class TweetDelete(LoginRequiredMixin, DeleteView):
    model = Tweet
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('tweet:list')
    # success_url = '/tweets/' # this will do the same thing as above

# function-based view for CreateView with user set to the current user

# def tweet_create(request):
#     form = TweetModelForm(request.POST or None)
#     if form.is_valid():
#         instance = form.save(commit=False)
#         instance.user = request.user
#         instance.save()
#     return render(request, 'create.html', {'form': form})

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
