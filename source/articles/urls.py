from django.urls import path

from articles.views import (
    ArticleDetailView,
    article_delete_view,
    ArticleListView,
    ArticleCreateView,
    ArticleUpdateView,
)

urlpatterns = [
    path("", ArticleListView.as_view(), name="list"),
    path("articles/add/", ArticleCreateView.as_view(), name="create"),
    path("article/<slug:slug>/", ArticleDetailView.as_view(), name="detail"),
    path("article/<int:pk>/update/", ArticleUpdateView.as_view(), name="update"),
    path("article/<int:pk>/delete/", article_delete_view, name="delete"),
]