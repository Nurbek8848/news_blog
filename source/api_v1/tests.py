from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from articles.models import Article


class ArticleLikeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="liker", password="test-password"
        )
        cls.article = Article.objects.create(
            title="Article for likes", author=cls.user
        )

    def test_post_toggles_like(self):
        self.client.force_login(self.user)
        url = reverse("api_v1:likes", kwargs={"pk": self.article.pk})

        first_response = self.client.post(url)
        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(first_response.json(), {"count": 1})
        self.assertTrue(self.article.likes.filter(pk=self.user.pk).exists())

        second_response = self.client.post(url)
        self.assertEqual(second_response.status_code, 200)
        self.assertEqual(second_response.json(), {"count": 0})
        self.assertFalse(self.article.likes.filter(pk=self.user.pk).exists())
