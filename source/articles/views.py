from django.http import HttpResponseRedirect
from django.shortcuts import render

from articles.articles_db import ArticlesDB


# Create your views here.


def articles(request):
    context = {
        "articles": ArticlesDB.articles,
    }
    return render(request, "index.html", context)


def article_create_view(request):
    if request.method == 'GET':
        return render(request, 'article_create.html')
    elif request.method == 'POST':
        new_article = {
            "title": request.POST.get("title"),
            "content": request.POST.get("content"),
            "author": request.POST.get("author"),
        }
        ArticlesDB.articles.append(new_article)
        return HttpResponseRedirect("/articles")