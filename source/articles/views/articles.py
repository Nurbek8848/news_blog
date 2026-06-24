from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import FormView, ListView, DetailView, CreateView, UpdateView, DeleteView

from articles.forms import ArticleForm, SimpleSearchForm, ArticleDeleteForm
from articles.models import Article


class ArticleListView(ListView):
    template_name = "articles/index.html"
    model = Article
    context_object_name = "articles"
    ordering = ["-created_at"]
    queryset = Article.objects.all()
    paginate_by = 4
    paginate_orphans = 1

    def dispatch(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().dispatch(request, *args, **kwargs)

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.search_value:
            queryset = queryset.filter(
                Q(title__icontains=self.search_value) | Q(author__icontains=self.search_value)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form

        if self.search_value:
            context['query'] = urlencode({"search": self.search_value})
            context['search_value'] = self.search_value
        return context



class ArticleDetailView(DetailView):
    template_name = "articles/article_view.html"
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(author='asdqwe')
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    template_name = "articles/article_create.html"
    form_class = ArticleForm


class ArticleUpdateView(UpdateView):
    template_name = "articles/article_update.html"
    form_class = ArticleForm
    model = Article
    # queryset = Article.objects.all()

    # def get_success_url(self):
    #     return reverse("detail", kwargs={"pk": self.object.pk})

class ArticleDeleteView(DeleteView):
    template_name = "articles/delete_confirm.html"
    model = Article
    form_class = ArticleDeleteForm
    success_url = reverse_lazy("articles:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if self.request.method == 'POST':
            kwargs['instance'] = self.object
        return kwargs

    # def post(self, request, *args, **kwargs):
    #     article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
    #     article.delete()
    #     return redirect("list")
