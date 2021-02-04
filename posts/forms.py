from django.forms import ModelForm, forms

from posts.models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['group', 'text', 'image']

    def validate_form(self):
        data = self.cleaned_data['text']
        if data is None:
            raise forms.ValidationError('Пост не может быть пустым')
