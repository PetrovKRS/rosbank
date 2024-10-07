from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.views import APIView
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
    EmployeeSerializer, DevelopmentPlanSerializer, IndividualDevelopmentPlanRequestSerializer, IndividualDevelopmentPlanResponseSerializer
)
from api.filters import (
    EmployeeFilter
)
from rest_framework.response import Response

class WorkersViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EmployeeFilter


class DevelopmentPlanViewSet(viewsets.ModelViewSet):
    queryset = DevelopmentPlan.objects.all()
    serializer_class = DevelopmentPlanSerializer

class MetricViewSet(viewsets.ViewSet):
    def create(self, request, metric_type):
        request_serializer = IndividualDevelopmentPlanRequestSerializer(data=request.data)

        if request_serializer.is_valid():
            employee_ids = request_serializer.validated_data['employeeIds']
            start_period = request_serializer.validated_data['startPeriod']
            end_period = request_serializer.validated_data['endPeriod']

            dashboard = []
            total_completion = 0

            # Определяем модель в зависимости от типа метрики
            model = None
            if metric_type == 'development_plan':
                model = EmployeeDevelopmentPlan
            elif metric_type == 'engagement':
                model = EmployeeEngagement
            else:
                return Response(
                    {"error": "Invalid metric type."},
                          status=status.HTTP_400_BAD_REQUEST
                )

            for employee_id in employee_ids:
                try:
                    # Получаем данные по выбранной модели
                    employee_metric = model.objects.get(employee__employee_id=employee_id)
                    performance = employee_metric.engagement_level if metric_type == 'engagement' else employee_metric.development_progress
                    dashboard.append({
                        "period": {
                            "month": start_period['month'],
                            "year": start_period['year']
                        },
                        "performance": str(performance)
                    })
                    total_completion += performance
                except model.DoesNotExist:
                    continue

            # Получаем данные за последний месяц
            completion_for_today = dashboard[-1]['performance'] if dashboard else "0.00"

            response_data = {
                "dashboard": dashboard,
                "completionForToday": completion_for_today
            }

            response_serializer = IndividualDevelopmentPlanResponseSerializer(data=response_data)
            response_serializer.is_valid(raise_exception=True)

            return Response(response_serializer.data, status=status.HTTP_200_OK)

        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
