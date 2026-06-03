from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from articles.forms import ArticleForm
from articles.models import Article
from articles.validators import validate_article


def articles(request):
    articles = Article.objects.all().order_by('-created_at')
    context = {'articles': articles}
    return render(request, "articles/index.html", context)


def article(request, *args, pk, **kwargs):
    article = get_object_or_404(Article, pk=pk)
    context = {'article': article}
    return render(request, "articles/article_view.html", context)


def article_create_view(request):
    form = ArticleForm()
    if request.method == 'GET':
        return render(request, 'articles/article_create.html', {'form': form})
    elif request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            return redirect("detail", pk=article.pk)
        else:
            return render(request, 'articles/article_create.html', {'form': form})
        # return redirect("list")


def article_update_view(request, pk, *args, **kwargs):
    article = get_object_or_404(Article, pk=pk)
    form = ArticleForm(instance=article)
    context = {'form': form}

    if request.method == 'GET':
        return render(request, 'articles/article_update.html', context)
    elif request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            return redirect("detail", pk=article.pk)
        return render(request, 'articles/article_update.html', {'form': form})


def article_delete_view(request, pk, *args, **kwargs):
    if request.method == 'POST':
        article = get_object_or_404(Article, pk=pk)
        article.delete()
    return redirect("list")
