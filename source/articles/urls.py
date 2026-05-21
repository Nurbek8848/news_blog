from django.urls import path

from articles.views import articles, article_create_view

urlpatterns = [
    path("", articles),
    path("add/", article_create_view),
]