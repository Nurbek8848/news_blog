from django.db import models


status_choices = [('new', 'Новая'), ('approved', 'Одобрено'),  ('Return_for_revision', 'Отправлено на доработку')]

class Blog(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name="Заголовок")
    content = models.TextField(max_length=5000, null=True, blank=True, verbose_name="Описание")

    def __str__(self):
        return self.title



class Article(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name="Заголовок")
    content = models.TextField(max_length=5000, null=True, blank=True, verbose_name="Описание")
    author = models.CharField(max_length=100, null=False, blank=False, verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата редактирования")
    status = models.CharField(max_length=25, choices=status_choices, default=status_choices[0][0], verbose_name="Статус")
    blog = models.ForeignKey("articles.Blog", on_delete=models.CASCADE, null=True, related_name="article")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Статьи"
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
