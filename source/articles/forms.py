from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple

from articles.models import Article


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content", "author", "tags"]

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
        fields = ["title", "content", "author", "tags", "status"]

        widgets = {
            'tags': CheckboxSelectMultiple(),
        }
