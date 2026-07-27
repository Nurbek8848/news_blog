from django.urls.conf import path

from api_v1.views import Test, get_token_view, Articlelike

app_name = 'api_v1'

urlpatterns = [
    path("test/", Test.as_view(), name="echo"),
    path("test/<int:pk>/", Test.as_view(), name="echo"),
    path("token/", get_token_view, name="token"),
    path("<int:pk>/likes/", Articlelike.as_view(), name="likes"),
]