from django.contrib import admin

from articles.models import Article, Tag, ArticleTag


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'created_at']
    list_filter = ['author']
    search_fields = ['title', 'content']
    fields = ['title', 'author', 'content', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']

admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
admin.site.register(ArticleTag)
