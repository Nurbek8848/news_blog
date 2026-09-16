from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from articles.models import Article, Comment, Tag


class ArticleApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.author = user_model.objects.create_user(
            username="api_author", password="test-password"
        )
        cls.other_user = user_model.objects.create_user(
            username="api_reader", password="test-password"
        )
        cls.tag = Tag.objects.create(title="API")
        cls.article = Article.objects.create(
            title="Existing article", content="Existing content", author=cls.author
        )

    def setUp(self):
        self.client = APIClient()

    def test_anonymous_user_cannot_list_articles(self):
        response = self.client.get(reverse("api_v2:articles-list"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_list_articles(self):
        self.client.force_authenticate(user=self.author)

        response = self.client.get(reverse("api_v2:articles-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["title"], self.article.title)

    def test_create_article_sets_current_user_as_author(self):
        self.client.force_authenticate(user=self.author)
        response = self.client.post(
            reverse("api_v2:articles-list"),
            {
                "title": "Created article",
                "content": "Created content",
                "tags": [self.tag.pk],
                "author": self.other_user.pk,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        article = Article.objects.get(title="Created article")
        self.assertEqual(article.author, self.author)
        self.assertQuerySetEqual(article.tags.all(), [self.tag])

    def test_create_article_rejects_short_title(self):
        self.client.force_authenticate(user=self.author)

        response = self.client.post(
            reverse("api_v2:articles-list"),
            {"title": "Tiny", "tags": []},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_only_author_can_update_article(self):
        url = reverse("api_v2:articles-detail", kwargs={"pk": self.article.pk})
        self.client.force_authenticate(user=self.other_user)

        denied = self.client.patch(url, {"title": "Changed title"}, format="json")

        self.assertEqual(denied.status_code, status.HTTP_403_FORBIDDEN)
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, "Existing article")

        self.client.force_authenticate(user=self.author)
        allowed = self.client.patch(url, {"title": "Changed title"}, format="json")

        self.assertEqual(allowed.status_code, status.HTTP_200_OK)
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, "Changed title")

    def test_article_comments_action_returns_comments(self):
        comment = Comment.objects.create(
            article=self.article, author=self.other_user, text="Useful comment"
        )
        self.client.force_authenticate(user=self.author)

        response = self.client.get(
            reverse("api_v2:articles-get-comments", kwargs={"pk": self.article.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{"id": comment.pk, "text": comment.text}])
