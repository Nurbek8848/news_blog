from django.urls.conf import path

from api_v1.views import Test, get_token_view

urlpatterns = [
    path("echo/", Test.as_view(), name="echo"),
    path("token/", get_token_view, name="token"),
]