from django.urls import include, path, re_path
from rest_framework import routers

from api.views import (
    MetricViewSet, EmployeesViewSet,
    TeamMetricViewSet, TeamCountEmployeeViewSet,
    TeamIndividualCompetenciesViewSet,
    CompetencyLevelViewSet, TeamSkillViewSet,
    IndividualSkillViewSet, SkillLevelViewSet,
)

from .views import DevelopmentPlan
from core.models import AssesmentSkill

router_v1 = routers.DefaultRouter()


router_v1.register(r'teams/(?P<team_slug>[\w-]+)/count_employees', TeamCountEmployeeViewSet, basename='count_employees')
router_v1.register(r'teams/(?P<team_slug>[\w-]+)/employees', EmployeesViewSet, basename='employees')
router_v1.register(r'metrics/(?P<metric_type>development_plan|involvement)/(?P<employee_id>\d+)', MetricViewSet, basename='metric')
# Добавить Получение оценки навыков сотрудника individual-skill-assessment
router_v1.register(r'teams/(?P<team_slug>[\w-]+)/(?P<metric_type>development_plan|involvement)', TeamMetricViewSet, basename='team_metric') # План развития вовлеченность команды


router_v1.register(r'teams/(?P<team_slug>[\w-]+)/individual_competencies(?:/(?P<employee_id>\d+))?', TeamIndividualCompetenciesViewSet, basename='individual_competencies')

router_v1.register(
    r'teams/(?P<team_slug>[\w-]+)/competencies_level(?:/(?P<employee_id>\d+))?',
    CompetencyLevelViewSet,  # Новый ViewSet для получения уровней компетенций
    basename='competency_level'
)
router_v1.register(r'teams/(?P<team_slug>[\w-]+)/skills/', TeamSkillViewSet, basename='teams-skills-avg')
router_v1.register(r'teams/media/individual-skills/', IndividualSkillViewSet, basename='individual')
router_v1.register(r'teams/(?P<team_slug>[\w-]+)/skills/level', SkillLevelViewSet, basename='skill-level')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    # path('teams/media/individual-skills/', IndividualSkillViewSet.as_view({'post': 'get_individual_skills'}), name='individual-average-skills'),
]