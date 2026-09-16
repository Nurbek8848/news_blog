from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from articles.forms import ArticleDeleteForm, ArticleForm
from articles.models import Article, Tag


class ArticleModelAndFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = get_user_model().objects.create_user(
            username="article_author", password="test-password"
        )
        cls.article = Article.objects.create(
            title="A valid article title",
            content="Article body",
            author=cls.author,
        )

    def test_new_article_has_default_status_and_detail_url(self):
        self.assertEqual(self.article.status, "new")
        self.assertEqual(
            self.article.get_absolute_url(),
            reverse("articles:detail", kwargs={"pk": self.article.pk}),
        )

    def test_article_form_rejects_short_title(self):
        form = ArticleForm(data={"title": "Short", "content": "Article body"})

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_article_form_rejects_equal_title_and_content(self):
        form = ArticleForm(
            data={"title": "Matching title", "content": "Matching title"}
        )

        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)

    def test_delete_form_requires_article_title(self):
        wrong_title = ArticleDeleteForm(
            data={"title": "Another article"}, instance=self.article
        )
        correct_title = ArticleDeleteForm(
            data={"title": self.article.title}, instance=self.article
        )

        self.assertFalse(wrong_title.is_valid())
        self.assertIn("title", wrong_title.errors)
        self.assertTrue(correct_title.is_valid())

    def test_tags_can_be_assigned_to_article(self):
        tag = Tag.objects.create(title="Django")

        self.article.tags.add(tag)

        self.assertQuerySetEqual(self.article.tags.all(), [tag])
