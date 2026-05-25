from django.shortcuts import render, get_object_or_404, redirect

from articles.models import Article


def articles(request):
    articles = Article.objects.all().order_by('-created_at')
    context = {'articles': articles}
    return render(request, "articles/index.html", context)


def article(request, *args, pk, **kwargs):
    article = get_object_or_404(Article, pk=pk)
    context = {'article': article}
    return render(request, "articles/article_view.html", context)


def article_create_view(request):
    if request.method == 'GET':
        return render(request, 'articles/article_create.html')
    elif request.method == 'POST':
        article = Article.objects.create(
            title=request.POST.get("title"),
            content=request.POST.get("content"),
            author=request.POST.get("author"),
        )
        return redirect("detail", pk=article.pk)
        # return redirect("list")