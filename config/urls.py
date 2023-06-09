
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from rest_framework import permissions, authtoken
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include, re_path
from products.views import login
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView

from rest_framework_swagger.views import get_swagger_view

from users.views import *

schema_view = get_swagger_view(title='Pastebin API')

schema_view = get_schema_view(
   openapi.Info(
      title="Smart Tizim API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from datetime import datetime
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer




urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/v1/auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    

    path('admin/', admin.site.urls),
    path('api/', include('products.urls'), name='api'),
    # path('swagger/', schema_view),

    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


    path('users/', include('users.urls')),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_authtoken.auth.AuthTokenAuthentication',
    ),
}