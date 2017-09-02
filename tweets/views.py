from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, TemplateView

from users.models import UserProfile
from .mixins import FormUserNeededMixin, UserOwnerMixin
from .forms import TweetModelForm
from .models import Tweet


class TweetListSkeleton(TemplateView):
    """
    Only provide page skeleton, do the listing by Ajax afterward.
    """
    template_name = "tweets/home.html"

    def get_context_data(self, **kwargs):
        context = super(TweetListSkeleton, self).get_context_data(**kwargs)
        context['create_form'] = TweetModelForm()
        context['create_url'] = reverse_lazy('tweets:create')
        context['users_data'] = [{
            'user': user,
            'is_following': UserProfile.custom_objects.is_following(self.request.user, user),
        } for user in get_user_model().objects
            .annotate(tweet_count=Count('tweet'))
            .order_by('-tweet_count')]
        return context


class TweetDetail(DetailView):
    model = Tweet
    template_name = "tweets/detail.html"

    def get_context_data(self, **kwargs):
        context = super(TweetDetail, self).get_context_data(**kwargs)
        context['is_following'] = UserProfile.custom_objects.is_following(self.request.user, self.get_object().user)
        return context


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


class TweetDelete(LoginRequiredMixin, DeleteView):
    model = Tweet
    template_name = 'tweets/delete_confirm.html'
    success_url = reverse_lazy('home')
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
