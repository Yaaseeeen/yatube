from django import forms

from posts.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'text', 'image')

    def validate_form(self):
        data = self.cleaned_data['text']
        if data is None:
            raise forms.ValidationError('Пост не может быть пустым')
