from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name="Заголовок")
    content = models.TextField(max_length=5000, null=True, blank=True, verbose_name="Описание")
    author = models.CharField(max_length=100, null=False, blank=False, verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата редактирования")
    moderated_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата модерации")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Статья"
        verbose_name = "Статья"
