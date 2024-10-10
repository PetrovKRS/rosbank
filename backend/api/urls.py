from django.urls import include, path, re_path
from rest_framework import routers

from api.views import (
    DevelopmentPlanViewSet, MetricViewSet, EmployeesViewSet,
    TeamMetricViewSet, TeamCountEmployeeViewSet, SkillAssessmentViewSet
)

from .views import DevelopmentPlan
from core.models import AssesmentSkill

router_v1 = routers.DefaultRouter()



router_v1.register(r'development_plan', DevelopmentPlanViewSet, basename='development_plan')
# router_v1.register(r'skills/(?P<skill_type>hard|soft)', SkillViewSet, basename='skill')
# процентов развития сколька планов развития

router_v1.register(r'teams/(?P<team_slug>[\w-]+)/count_employees', TeamCountEmployeeViewSet, basename='count_employees')
router_v1.register(r'teams/(?P<team_slug>[\w-]+)/employees', EmployeesViewSet, basename='employees')
router_v1.register(r'metrics/(?P<metric_type>development_plan|involvement)', MetricViewSet, basename='metric')# Добавить Получение оценки навыков сотрудника individual-skill-assessment
router_v1.register(r'teams/(?P<team_slug>[\w-]+)/(?P<metric_type>development_plan|involvement)', TeamMetricViewSet, basename='team_metric') # План развития вовлеченность команды

# Маршрут для получения средних значений навыков команды
router_v1.register(r'teams/media/skills', SkillAssessmentViewSet, basename='team-skill-assessment')
# Маршрут для получения средних значений навыков сотрудника
router_v1.register(r'teams/media/individual-skills', SkillAssessmentViewSet, basename='individual-skill-assessment')
# Маршрут для получения уровня навыка сотрудника
router_v1.register(r'teams/media/skills/level', SkillAssessmentViewSet, basename='skill-level-assessment')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    # path('auth/', include('djoser.urls')),
    # re_path('auth/', include('djoser.urls.authtoken')),
]