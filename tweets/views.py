from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .mixins import FormUserNeededMixin, UserOwnerMixin
from .forms import TweetModelForm
from .models import Tweet


class TweetList(ListView):
    template_name = "tweets/home.html"

    def get_queryset(self):
        qs = Tweet.objects.all().order_by('-created_at')
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(Q(content__icontains=query) | Q(user__username__icontains=query))
        return qs

    def get_context_data(self, **kwargs):
        context = super(TweetList, self).get_context_data(**kwargs)
        context['create_form'] = TweetModelForm()
        context['create_url'] = reverse_lazy('tweets:create')
        return context


class TweetDetail(DetailView):
    model = Tweet
    template_name = "tweets/detail.html"


class TweetCreate(FormUserNeededMixin, CreateView):
    form_class = TweetModelForm
    # if don't use form_class
    # model = Tweet
    # fields = [
    #     'content'
    # ]

    template_name = "tweets/create.html"


class TweetUpdate(LoginRequiredMixin, UserOwnerMixin, UpdateView):
    model = Tweet
    form_class = TweetModelForm
    template_name = "tweets/update.html"
    login_url = '/admin/'


class TweetDelete(LoginRequiredMixin, DeleteView):
    model = Tweet
    template_name = 'tweets/delete_confirm.html'
    success_url = reverse_lazy('tweets:list')
    # success_url = '/tweets/' # this will do the same thing as above

# function-based view for CreateView with user set to the current user

# def tweet_create(request):
#     form = TweetModelForm(request.POST or None)
#     if form.is_valid():
#         instance = form.save(commit=False)
#         instance.user = request.user
#         instance.save()
#     return render(request, 'tweets/create.html', {'form': form})

# function-based views of list and detail views

# def tweet_detail_view(request, id):
#     context = {
#         'object': Tweet.objects.get(id=id)
#     }
#     return render(request, 'tweets/detail.html', context)
#
# def tweet_list_view(request):
#     context = {
#         'object_list': Tweet.objects.all()
#     }
#     return render(request, 'tweets/home.html', context)
