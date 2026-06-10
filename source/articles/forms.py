from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets, ModelForm, CharField
from django.core.validators import MinLengthValidator, MinValueValidator
from articles.models import Article, Tag
from articles.models.article import status_choices


class ArticleForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].widget.attrs.update({
            "style": "min-height: 120px",
        })

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    title = forms.CharField(
        widget=widgets.TextInput(),
        required=True,
        label="Заголовок",
        error_messages={"required": "Загловок обязательное поле"},
        validators=[MinLengthValidator(3)],
    )
    content = forms.CharField(
        widget=widgets.Textarea(),
        required=False,
        label="Описание",
    )
    author = forms.CharField(
        widget=widgets.TextInput(),
        required=True,
        label="Автор",
    )
    status = forms.ChoiceField(
        choices=status_choices,
        widget=widgets.Select()
    )
    # tags = forms.ModelMultipleChoiceField(
    #     queryset=Tag.objects.all(),
    #     required=False,
    #     widget=widgets.SelectMultiple()
    # )
    tags = forms.CharField(
        widget=widgets.TextInput(),
        required=False,
    )

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        cleaned_tags = []

        if tags:
            tags = tags.split(',')

            for tag_str in tags:
                tag = Tag.objects.filter(title__iexact=tag_str.strip()).first()

                if not tag:
                    tag = Tag.objects.create(title=tag_str.strip())
                cleaned_tags.append(tag)
        return cleaned_tags

    def set_initial_tags(self, tags):
        self.fields['tags'].initial = ", ".join([tag.title for tag in tags])


# class ArticleForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # self.fields["content"].widget.attrs.update({
#         #     "style": "min-height: 120px",
#         # })
#
#         # for field in self.fields.values():
#         #     field.widget.attrs['class'] = 'form-control'
#
#
#     class Meta:
#         model = Article
#         fields = ["title", "content", "author", "status", "tags"]
#
#         # widgets = {
#         #     "content": widgets.Textarea(attrs={"cols": "40", "rows": "5"}),
#         # }
#
#     def clean(self):
#         title = self.cleaned_data.get("title")
#         content = self.cleaned_data.get("content")
#
#         if title and content and title == content:
#             raise ValidationError("Заголовок и описание не могут быть похожи")
#         return super().clean()
#
#     def clean_title(self):
#         title = self.cleaned_data.get("title")
#
#         if title and "102" in title:
#             raise ValidationError("Недопустимый заголовок")
#         return title
#
#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         blog = self.cleaned_data["blog"]
#         instance.blog = blog
#         instance.save()
#         self.save_m2m()
#         return instance