from django.shortcuts import get_object_or_404
from django.views.generic import CreateView

from articles.forms import CommentForm
from articles.models import Article, Comment


class CommentCreateView(CreateView):
    template_name = "comments/comment_create.html"
    form_class = CommentForm
    model = Comment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_pk'] = self.kwargs.get('pk')
        return context

    def form_valid(self, form):
        artice = get_object_or_404(Article, pk=self.kwargs["pk"])
        form.instance.article = artice
        form.instance.author = self.request.user
        return super().form_valid(form)
