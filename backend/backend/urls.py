from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from django.urls import path, include


schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation R-Bank",
        default_version='v1',
        description="Документация для проекта Ros-Bank",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="your-email@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url="https://rosb-hakaton.ddns.net",
    # schemes=['https'],  # Ограничьте схемы только https
)


urlpatterns = (
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=5),
        name='schema-swagger-ui',
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc',
    ),
    # path('auth/', include('djoser.urls')),
    # # JWT-эндпоинты, для управления JWT-токенами:
    # path('auth/', include('djoser.urls.authtoken')),       # JWT-эндпоинты
)
