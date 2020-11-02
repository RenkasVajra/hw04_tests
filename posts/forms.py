from django import forms

from django.forms import ModelForm

from . import views
from posts.models import Post 





class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = {'group', 'text',}
        labels = {
            'group': 'Группа',
            'text': 'Текст',
        }
        help_text = {'name': 'Создайте свой новый пост.'}