from django.urls import path

from articles.views import (
    ArticleDetailView,
    ArticleDeleteView,
    ArticleListView,
    ArticleCreateView,
    ArticleUpdateView,
    CommentCreateView,
)

app_name = "articles"
urlpatterns = [
    path("", ArticleListView.as_view(), name="list"),
    path("articles/add/", ArticleCreateView.as_view(), name="create"),
    path("article/<int:pk>/", ArticleDetailView.as_view(), name="detail"),
    path("article/<int:pk>/update/", ArticleUpdateView.as_view(), name="update"),
    path("article/<int:pk>/delete/", ArticleDeleteView.as_view(), name="delete"),
    path("article/<int:pk>/comment-add/", CommentCreateView.as_view(), name="comment-create"),
]