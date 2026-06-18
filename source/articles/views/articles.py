from urllib.parse import urlencode

from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import FormView, ListView, DetailView, CreateView

from articles.forms import ArticleForm, SimpleSearchForm
from articles.models import Article, Tag


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
        self.tag = self.request.GET.get("tag")
        print(self.tag)
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

        if self.tag:
            queryset = queryset.filter(tags__id=self.tag)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form
        context['tags'] = Tag.objects.all()
        query_params = {}

        if self.search_value:
            query_params.update({"search": self.search_value})
            context['search_value'] = self.search_value

        if self.tag:
            query_params.update({"tag": self.tag})
            context['tag'] = self.tag

        if query_params:
            context['query'] = urlencode(query_params)
        return context



class ArticleDetailView(DetailView):
    template_name = "articles/article_view.html"
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(author='asdqwe')
        context['tags'] = Tag.objects.all()
        return context


class ArticleCreateView(CreateView):
    template_name = "articles/article_create.html"
    form_class = ArticleForm
    # success_url = reverse_lazy("list")
    # extra_context = {'tags': Tag.objects.all()}

    def get_success_url(self):
        return reverse("detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context


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
