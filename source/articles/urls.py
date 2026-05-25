from django.urls import path

from articles.views import articles, article_create_view, article

urlpatterns = [
    path("articles/", articles),
    path("articles/add/", article_create_view),
    path("article/<int:pk>/", article),
]