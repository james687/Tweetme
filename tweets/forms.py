from django import forms

from .models import Tweet


class TweetModelForm(forms.ModelForm):
    # NOTE this property needs to be exactly the same name the `content` field below to override its default setting
    content = forms.CharField(label='',
                              widget=forms.Textarea(
                                  attrs={'placeholder': "What's happening?",
                                         "class": "form-control",
                                         'rows': 3}
                              ))

    class Meta:
        model = Tweet
        fields = [
            'content'
        ]
