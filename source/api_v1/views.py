import json
from datetime import datetime

from django.http.response import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import View

from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from api_v1.serializers import ArticleSerializer
from articles.models import Article, article


# def json_echo_view(request, *args, **kwargs):
#     answer = {
#         'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#         'method': request.method,
#     }
#     answer_as_json = json.dumps(answer)
#     response = HttpResponse(answer_as_json)
#     # response['Content-Type'] = 'application/json'
#     return response

# class Test(View):
#     def get(self, request, *args, **kwargs):
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)
#         return JsonResponse(serializer.data, safe=False)
#
#     def post(self, request, *args, **kwargs):
#         if request.body:
#             data = json.loads(request.body)
#             serializer = ArticleSerializer(data=data)
#
#             if serializer.is_valid():
#                 serializer.save(author=request.user)
#                 return JsonResponse(serializer.data, status=201, safe=False)
#             return JsonResponse(serializer.errors, status=400)
#
#     def put(self, request, pk, *args, **kwargs):
#         article = get_object_or_404(Article, id=pk)
#         if request.body:
#             data = json.loads(request.body)
#             serializer = ArticleSerializer(data=data, instance=article)
#
#             if serializer.is_valid():
#                 serializer.save()
#                 return JsonResponse(serializer.data, status=200, safe=False)
#             return JsonResponse(serializer.errors, status=400)


class Test(APIView):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        tags = request.data.pop('tags', [])
        serializer = ArticleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user, tags=tags)
        return Response(serializer.data, status=201)

    def put(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, id=pk)
        tags = request.data.pop('tags', [])
        serializer = ArticleSerializer(data=request.data, instance=article)
        serializer.is_valid(raise_exception=True)
        serializer.save(tags=tags)
        return JsonResponse(serializer.data, status=200)



class Articlelike(View):
    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, id=self.kwargs.get('pk'))
        if article in request.user.liked_articles.all():
            article.likes.remove(request.user)
        else:
            article.likes.add(request.user)

        return JsonResponse({'count': article.likes.count()})


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')
