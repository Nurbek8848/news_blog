from django.core.exceptions import ValidationError
from django.forms import widgets, ModelForm
from django.core.validators import EmailValidator
from articles.models import Article, Blog


class ArticleForm(ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     for field in self.fields.values():
    #         field.widget.attrs['class'] = 'form-control'


    class Meta:
        model = Article
        fields = ["title", "content", "author", "status", "blog"]

        widgets = {
            "content": widgets.Textarea(attrs={"cols": "40", "rows": "5"}),
        }

    def clean(self):
        title = self.cleaned_data.get("title")
        content = self.cleaned_data.get("content")

        if title and content and title == content:
            raise ValidationError("Заголовок и описание не могут быть похожи")
        return super().clean()

    def clean_title(self):
        title = self.cleaned_data.get("title")

        if title and "102" in title:
            raise ValidationError("Недопустимый заголовок")
        return title

    def save(self, commit=True):
        instance = super().save(commit=False)
        blog = self.cleaned_data["blog"]
        instance.blog = blog
        instance.save()
        return instance