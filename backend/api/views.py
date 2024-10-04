from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework import (
    mixins,
    permissions,
    status,
    viewsets,
    exceptions,
    generics
)
from users.models import (
   Employee,
)
from core.models import (
    DevelopmentPlan, EmployeeDevelopmentPlan, EmployeeEngagement,
    KeyPeople, EmployeeKeyPeople, TrainingApplication, EmployeeTrainingApplication,
    BusFactor, EmployeeBusFactor, Grade, EmployeeGrade, KeySkill, EmployeeKeySkill,
    Team, EmployeeTeam, Position, EmployeePosition, Competency, PositionCompetency,
    TeamPosition, EmployeeCompetency, Skill, EmployeeSkill, SkillForCompetency,
    ExpectedSkill, EmployeeExpectedSkill, CompetencyForExpectedSkill
)
from .serializers import (
    EmployeeSerializer
)
from api.filters import (
    EmployeeFilter
)

# Create your views here.
class WorkersViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EmployeeFilter
    
