from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from ..views.jwt_views import Jwt_view

urlpatterns = [
       path('token/refresh', Jwt_view.RefreshTokenView, name='token_refresh'),
]