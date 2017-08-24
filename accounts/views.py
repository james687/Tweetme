from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

User = get_user_model()


class UserDetailView(DetailView):
    model = User
    template_name = 'accounts/detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(User, username__iexact=self.kwargs.get('username'))