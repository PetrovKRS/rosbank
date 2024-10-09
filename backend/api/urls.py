from django.urls import include, path, re_path
from rest_framework import routers

from api.views import (
    DevelopmentPlanViewSet, MetricViewSet, EmployeesViewSet, TeamMetricViewSet
)

from .views import DevelopmentPlan, SkillViewSet
from core.models import AssesmentSkill

router_v1 = routers.DefaultRouter()


router_v1.register(r'teams/(?P<team_slug>[\w-]+)/employees', EmployeesViewSet, basename='employees')
router_v1.register(r'development_plan', DevelopmentPlanViewSet, basename='development_plan')
router_v1.register(r'metrics/(?P<metric_type>development_plan|engagement|employees)', MetricViewSet, basename='metric')
router_v1.register(r'skills/(?P<skill_type>hard|soft)', SkillViewSet, basename='skill')
router_v1.register(r'team_metrics', TeamMetricViewSet, basename='team_metric')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    # path('auth/', include('djoser.urls')),
    # re_path('auth/', include('djoser.urls.authtoken')),
]