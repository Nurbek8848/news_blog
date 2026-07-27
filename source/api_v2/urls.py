from django.urls import include
from django.urls.conf import path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from api_v2.views import ArticleViewSet

app_name = 'api_v2'

router = routers.DefaultRouter()
router.register(r'articles', ArticleViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path('login/', obtain_auth_token, name='api_token_auth')
]