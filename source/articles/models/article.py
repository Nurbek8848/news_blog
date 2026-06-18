from django.db import models
from django.urls import reverse

from articles.models import BaseModel


status_choices = [('new', 'Новая'), ('approved', 'Одобрено'),  ('Return_for_revision', 'Отправлено на доработку')]


class Article(BaseModel):
    title = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        verbose_name="Заголовок"
    )
    content = models.TextField(
        max_length=5000,
        null=True,
        blank=True,
        verbose_name="Описание"
    )
    author = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name="Автор"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата редактирования"
    )
    status = models.CharField(
        max_length=25,
        choices=status_choices,
        default=status_choices[0][0],
        verbose_name="Статус"
    )
    tags = models.ManyToManyField(
        "articles.Tag",
        related_name="articles",
        blank=True,
        through="articles.ArticleTag",
        through_fields=("article", "tag"),
        verbose_name="Теги"
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Article"
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk": self.pk})

class ArticleTag(BaseModel):
    article = models.ForeignKey(
        "articles.Article",
        on_delete=models.CASCADE,
        null=True,
        related_name="articles_tags"
    )
    tag = models.ForeignKey(
        "articles.Tag",
        on_delete=models.CASCADE,
        null=True,
        related_name="tags_articles"
    )
    is_active = models.BooleanField(
        default=True
    )
