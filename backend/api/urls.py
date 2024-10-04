from django.urls import include, path
from rest_framework import routers

from .views import (
    EmployeeViewSet
)

app_name = 'api'

router = routers.DefaultRouter()

router.register(r'workers', EmployeeViewSet, basename='workers')
