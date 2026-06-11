from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView

from articles.forms import ArticleForm
from articles.models import Article


class ArticleListView(TemplateView):
    template_name = "articles/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.all().order_by('-created_at')
        return context


class ArticleDetailView(TemplateView):
    template_name = "articles/article_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        return context


class ArticleCreateView(FormView):
    template_name = "articles/article_create.html"
    form_class = ArticleForm
    success_url = reverse_lazy("list")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ArticleUpdateView(FormView):
    template_name = "articles/article_update.html"
    form_class = ArticleForm

    def dispatch(self, request, *args, **kwargs):
        self.article = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(Article, pk=self.kwargs.get('pk'))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.article
        return kwargs

    def form_valid(self, form):
        article = form.save()
        return redirect("detail", pk=article.pk)

class ArticleDeleteView(View):
    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        article.delete()
        return redirect("list")
