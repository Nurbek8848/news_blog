from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from articles.models import BaseModel


class Comment(BaseModel):
    article = models.ForeignKey('articles.Article', related_name='comments', on_delete=models.CASCADE,
                                verbose_name='Статья')
    text = models.TextField(max_length=400, verbose_name='Комментарий')
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        related_name="comments",
        verbose_name="Автор"
    )

    def __str__(self):
        return self.text[:20]

    def get_absolute_url(self):
        return reverse("articles:detail", kwargs={"pk": self.article.pk})
