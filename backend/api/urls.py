from django.urls import include, path
from rest_framework import routers

from api.views import (
    MetricViewSet,
    EmployeesViewSet,
    TeamMetricViewSet,
    TeamCountEmployeeViewSet,
    TeamIndividualCompetenciesViewSet,
    TeamIndividualSkillsViewSet,
    CompetencyLevelViewSet,
    SkillLevelViewSet,
)

from core.models import AssesmentSkill

router_v1 = routers.DefaultRouter()

router_v1.register(
    r'teams/(?P<team_slug>[\w-]+)/count_employees',
    TeamCountEmployeeViewSet,
    basename='count_employees',
)
router_v1.register(
    r'teams/(?P<team_slug>[\w-]+)/employees',
    EmployeesViewSet,
    basename='employees',
)
router_v1.register(
    r'metrics/(?P<metric_type>development_plan|involvement)/(?P<employee_id>\d+)',
    MetricViewSet,
    basename='metric',
)

router_v1.register(
    r'teams/(?P<team_slug>[\w-]+)/(?P<metric_type>development_plan|involvement)',
    TeamMetricViewSet,
    basename='team_metric',
)


router_v1.register(
    r'teams/(?P<team_slug>[\w-]+)/individual_competencies(?:/(?P<employee_id>\d+))?',
    TeamIndividualCompetenciesViewSet,
    basename='individual_competencies',
)

router_v1.register(
    r'teams/(?P<team_slug>[\w-]+)/competencies_level(?:/(?P<employee_id>\d+))?',
    CompetencyLevelViewSet,
    basename='competency_level',
)
router_v1.register(
    r'teams/(?P<team_slug>[\w-]+)/skills(?:/(?P<employee_id>\d+))?',
    TeamIndividualSkillsViewSet,
    basename='skills',
)
router_v1.register(
    r'teams/(?P<team_slug>[\w-]+)/skills/level',
    SkillLevelViewSet,
    basename='skill-level',
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
