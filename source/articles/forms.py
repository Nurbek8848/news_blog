from django import forms
from django.forms import Textarea, TextInput

from articles.models import Article


class ArticleForm(forms.Form):
    title = forms.CharField(widget=TextInput(attrs={"class": "form-control"}), required=True, label="Заголовок", error_messages={"required": "Загловок обязательное поле"})
    content = forms.CharField(widget=Textarea(attrs={"class": "form-control","cols": "40", "rows": "5"}), required=False, label="Описание")
    author = forms.CharField(widget=TextInput(attrs={"class": "form-control"}), required=True, label="Автор")


# class ArticleForm(forms.ModelForm):
#
#     class Meta:
#         model = Article
#         fields = ["title", "content", "author"]
