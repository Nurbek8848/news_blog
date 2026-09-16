from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token


class RegistrationTests(TestCase):
    def test_registration_creates_user_and_api_token(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "new_reader",
                "password1": "Strong-test-password-123",
                "password2": "Strong-test-password-123",
                "first_name": "New",
                "last_name": "Reader",
                "email": "reader@example.com",
            },
        )

        self.assertRedirects(response, reverse("articles:list"))
        user = get_user_model().objects.get(username="new_reader")
        token = Token.objects.get(user=user)
        self.assertEqual(response.cookies["token"].value, token.key)
