from django.urls import include, path
from rest_framework import routers

from .views import (
    WorkersViewSet
)

app_name = 'api'

router = routers.DefaultRouter()

router.register(r'workers/list', WorkersViewSet, basename='workers')

urlpatterns = [
    path('/', include('router.urls'))
]
