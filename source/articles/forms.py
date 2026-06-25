from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple

from articles.models import Article, Comment


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content", "tags"]
        widgets = {
            'tags': CheckboxSelectMultiple(),
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        content = cleaned_data.get("content")

        if title and content and title == content:
            raise ValidationError("Заголовок и описание не могут быть похожи")
        return cleaned_data


    def clean_title(self):
        title = self.cleaned_data['title']

        if len(title) < 10:
            raise ValidationError('Title is too short!')

        return title


class ArticleStatusForm(ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content", "tags", "status"]

        widgets = {
            'tags': CheckboxSelectMultiple(),
        }


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="")


class ArticleDeleteForm(ModelForm):
    class Meta:
        model = Article
        fields = ["title"]

    def clean_title(self):
        title = self.cleaned_data['title']

        if title == self.instance.title:
            return title
        raise ValidationError("Название статьи не совпадает с оригиналом")


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
