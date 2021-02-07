from django import forms
from django.forms import ModelForm

from posts.models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'text', 'image')
        labels = {
            'text': 'Текст поста',
            'group': 'Группа',
            'image': 'Изображение',
        }
        error_messages = {'image': {'invalid': 'invalid type'}}
        help_texts = {'text': 'Добавьте текст(обязательно)', 'group': 'Выберите группу(опционально)',
                      'image': 'Выберите картинку(опционально)', }

    def validate_form(self):
        data = self.cleaned_data['text']
        if data is None:
            raise forms.ValidationError('Пост не может быть пустым')


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            'text': 'Текст комментария',
        }
        help_texts = {'text': 'Добавьте комментарий'}
