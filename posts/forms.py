from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post

        fields = ['text', 'group']
        labels = {'text': 'Введите текст', 'group': 'Выберите группу'}
        help_texts = {'text': 'Заполнить', 'group':
                                  'Выбрать группу'}


class EditPostForm(ModelForm):
    class Meta:
        model = Post

        fields = ['text', 'group']
        labels = {'text': 'Введите текст', 'group': 'Выберите группу'}
        help_texts = {'text': 'Заполнить', 'group':
                                  'Выбрать группу'}