import json
from datetime import datetime

from django.http.response import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import View

from articles.models import Article


# def json_echo_view(request, *args, **kwargs):
#     answer = {
#         'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#         'method': request.method,
#     }
#     answer_as_json = json.dumps(answer)
#     response = HttpResponse(answer_as_json)
#     # response['Content-Type'] = 'application/json'
#     return response

class Test(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.all()
        fields = ("id", "author", "title", "content")
        answer = articles.values_list(*fields)
        # answer = {
        #     'time': datetime.now(),
        #     'method': request.method,
        #     'article': {
        #         'id': article.id,
        #         'title': article.title,
        #     }
        # }

        return JsonResponse(list(answer), safe=False)

    def post(self, request, *args, **kwargs):
        answer = {}
        if request.body:
            data = json.loads(request.body)
            data['author'] = request.user
            article = Article.objects.create(**data)
            answer['article'] = article.id
        return JsonResponse(answer, status=201)

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'method': 'DELETE'})

    def patch(self, request, *args, **kwargs):
        return JsonResponse({'method': 'PATCH'})

    def put(self, request, *args, **kwargs):
        return JsonResponse({'method': 'PUT'})

@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')
