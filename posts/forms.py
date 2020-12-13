from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post

        fields = ['text', 'group']
        labels = {'text': 'Введите текст', 'group': 'Выберите группу'}


    def clean_text(self):
        data = self.cleaned_data['text']

        if 'text' == '':
            raise forms.ValidationError('Поле "текст" не заполнено')

        return data
