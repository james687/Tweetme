from django.conf import settings
from django.db import models
from django.urls import reverse


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='followed_by')

    def __str__(self):
        return '%s(following %d user(s))' % (self.user.username, self.following.all().count())

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.user.username})
