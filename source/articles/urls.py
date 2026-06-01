from django.urls import path

from articles.views import articles, article_create_view, article

urlpatterns = [
    path("articles/", articles, name="list"),
    path("", articles, name="list"),
    path("articles/add/", article_create_view, name="create"),
    path("article/<int:pk>/", article, name="detail"),
]