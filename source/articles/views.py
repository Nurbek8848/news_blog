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


class ArticleDetailView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        return context


class ArticleCreateView(View):
    def get(self, request, *args, **kwargs):
        form = ArticleForm()
        return render(request, 'articles/article_create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ArticleForm(request.POST)

        if form.is_valid():
            article = form.save()
            article.tags.set(form.cleaned_data['tags'])
            return redirect("detail", pk=article.pk)
        return render(request, 'articles/article_create.html', {'form': form})


class ArticleUpdateView(View):
    def dispatch(self, request, *args, **kwargs):
        self.article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        form = ArticleForm(instance=self.article)
        context = {'form': form}
        return render(request, 'articles/article_update.html', context)

    def post(self, request, *args, **kwargs):
        form = ArticleForm(request.POST, instance=self.article)

        if form.is_valid():
            article = form.save()
            article.tags.set(form.cleaned_data['tags'])
            article.save()
            return redirect("detail", pk=article.pk)
        return render(request, 'articles/article_update.html', {'form': form})

class ArticleDeleteView(View):
    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        article.delete()
        return redirect("list")
