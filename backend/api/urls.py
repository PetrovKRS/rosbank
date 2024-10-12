from django.urls import include, path, re_path
from rest_framework import routers

from api.views import (
    MetricViewSet, EmployeesViewSet,
    TeamMetricViewSet, TeamCountEmployeeViewSet,
    TeamIndividualCompetenciesViewSet,
    CompetencyLevelViewSet
)

from .views import DevelopmentPlan
from core.models import AssesmentSkill

router_v1 = routers.DefaultRouter()


router_v1.register(r'teams/(?P<team_slug>[\w-]+)/count_employees', TeamCountEmployeeViewSet, basename='count_employees')
router_v1.register(r'teams/(?P<team_slug>[\w-]+)/employees', EmployeesViewSet, basename='employees')
router_v1.register(r'metrics/(?P<metric_type>development_plan|involvement)', MetricViewSet, basename='metric')# Добавить Получение оценки навыков сотрудника individual-skill-assessment
router_v1.register(r'teams/(?P<team_slug>[\w-]+)/(?P<metric_type>development_plan|involvement)', TeamMetricViewSet, basename='team_metric') # План развития вовлеченность команды


router_v1.register(r'teams/(?P<team_slug>[\w-]+)/individual_competencies(?:/(?P<employee_id>\d+))?', TeamIndividualCompetenciesViewSet, basename='individual_competencies')
# Какого хуя я не могу сделать эндпоинт без (?P<employee_id>\d+)!!!
router_v1.register(
    r'teams/(?P<team_slug>[\w-]+)/competencies_level(?:/(?P<employee_id>\d+))?',
    CompetencyLevelViewSet,  # Новый ViewSet для получения уровней компетенций
    basename='competency_level'
)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    # path('auth/', include('djoser.urls')),
    # re_path('auth/', include('djoser.urls.authtoken')),
]