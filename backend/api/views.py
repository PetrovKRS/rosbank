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


class WorkersViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EmployeeFilter

    def post(self, request, *args, **kwargs):
        criterion = request.data.get('criterion')
        execution_data = request.data.get('executionData', [])

        # Находим работников, соответствующих критериям
        workers = Employee.objects.all()

        # Фильтруем по каждому месяцу и году
        for data in execution_data:
            month = data.get('month')
            year = data.get('year')
            workers = workers.filter(development_plans__month=month, development_plans__year=year)

        # Если указан критерий, фильтруем по навыку
        if criterion:
            workers = workers.filter(development_plans__key_skill__name__icontains=criterion)

        # Сериализация и возврат данных
        serializer = self.get_serializer(workers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)