from django.db import models

class Tag(models.Model):
    title = models.CharField(max_length=20, null=False, blank=False, verbose_name="Название")


    def __str__(self):
        return self.title

    class Meta:
        db_table = "Tags"
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
