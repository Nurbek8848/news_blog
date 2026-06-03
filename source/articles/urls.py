from django.urls import path

from articles.views import articles, article_create_view, article, article_update_view, article_delete_view

urlpatterns = [
    path("articles/", articles, name="list"),
    path("", articles, name="list"),
    path("articles/add/", article_create_view, name="create"),
    path("article/<int:pk>/", article, name="detail"),
    path("article/<int:pk>/update/", article_update_view, name="update"),
    path("article/<int:pk>/delete/", article_delete_view, name="delete"),
]