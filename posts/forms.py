from django import forms
from django.forms import Textarea

from posts.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'text', 'image')

    def validate_form(self):
        data = self.cleaned_data['text']
        if data is None:
            raise forms.ValidationError('Пост не может быть пустым')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

        widgets = {
            'text': Textarea(attrs={"class": "form-control"})
        }
# message = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control"}))
