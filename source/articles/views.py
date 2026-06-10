from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView

from articles.forms import ArticleForm
from articles.models import Article


class ArticleListView(TemplateView):
    template_name = "articles/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.all().order_by('-created_at')
        return context


class ArticleDetailView(View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, slug=self.kwargs.get('slug'))
        context = {'article': article}
        return render(request, "articles/article_view.html", context)


class ArticleCreateView(View):
    def get(self, request, *args, **kwargs):
        form = ArticleForm()
        return render(request, 'articles/article_create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ArticleForm(request.POST)

        if form.is_valid():
            article = Article(
                title=form.cleaned_data.get("title"),
                content=form.cleaned_data.get("content"),
                author=form.cleaned_data.get("author"),
            )
            article.save()
            article.tags.set(form.cleaned_data['tags'])
            return redirect("detail", pk=article.pk)
        return render(request, 'articles/article_create.html', {'form': form})


class ArticleUpdateView(View):
    def dispatch(self, request, *args, **kwargs):
        self.article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        form = ArticleForm(
            initial={
                'title': self.article.title,
                'author': self.article.author,
                'content': self.article.content,
                # 'tags': self.article.tags.all()
            })
        form.set_initial_tags(self.article.tags.all())
        context = {'form': form}
        return render(request, 'articles/article_update.html', context)

    def post(self, request, *args, **kwargs):
        form = ArticleForm(request.POST)

        if form.is_valid():
            self.article.title = form.cleaned_data.get("title")
            self.article.content = form.cleaned_data.get("content")
            self.article.author = form.cleaned_data.get("author")
            self.article.tags.set(form.cleaned_data['tags'])
            self.article.save()
            return redirect("detail", pk=self.article.pk)
        return render(request, 'articles/article_update.html', {'form': form})


def article_delete_view(request, pk, *args, **kwargs):
    if request.method == 'POST':
        article = get_object_or_404(Article, pk=pk)
        article.delete()
    return redirect("list")
