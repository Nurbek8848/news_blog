from django.db import models
from django.urls import reverse

from articles.models import BaseModel


class Comment(BaseModel):
    article = models.ForeignKey('articles.Article', related_name='comments', on_delete=models.CASCADE,
                                verbose_name='Статья')
    text = models.TextField(max_length=400, verbose_name='Комментарий')
    author = models.CharField(max_length=40, null=True, blank=True, default='Аноним', verbose_name='Автор')

    def __str__(self):
        return self.text[:20]

    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk": self.article.pk})
