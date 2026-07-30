from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, SAFE_METHODS
from rest_framework.response import Response

from api_v2.permissions import IsAuthorOrReadOnly
from api_v2.serializers import ArticleSerializer, ArticleShortSerializer, CommentSerializer
from articles.models import Article
from news_blog.services import MyPagination


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = MyPagination
    # permission_classes = [IsAuthenticatedOrReadOnly]
    permission_classes = [IsAuthorOrReadOnly]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAuthorOrReadOnly()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ArticleShortSerializer
        return ArticleSerializer

    @action(methods=['get'], detail=True, url_path='comments')
    def get_comments(self, request, *args, **kwargs):
         article = self.get_object()
         comments = article.comments.all()
         serializer = CommentSerializer(comments, many=True)
         return Response(serializer.data)