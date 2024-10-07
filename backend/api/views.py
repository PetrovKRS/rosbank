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
    ManagerTeam,
)
from core.models import (
    DevelopmentPlan, EmployeeDevelopmentPlan, EmployeeEngagement,
    KeyPeople, EmployeeKeyPeople, TrainingApplication, EmployeeTrainingApplication,
    BusFactor, EmployeeBusFactor, Grade, EmployeeGrade, KeySkill, EmployeeKeySkill,
    Team, EmployeeTeam, Position, EmployeePosition, Competency, PositionCompetency,
    TeamPosition, EmployeeCompetency, Skill, EmployeeSkill, SkillForCompetency,
    ExpectedSkill, EmployeeExpectedSkill, CompetencyForExpectedSkill, Employee
)
from .serializers import (
    EmployeeSerializer, DevelopmentPlanSerializer, IndividualDevelopmentPlanRequestSerializer, IndividualDevelopmentPlanResponseSerializer, MetricRequestSerializer
)
# from api.filters import (
#     EmployeeFilter
# )
from rest_framework.response import Response
from django.db.models import Avg

# class WorkersViewSet(viewsets.ModelViewSet):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
#     filter_backends = (filters.DjangoFilterBackend,)
#     filterset_class = EmployeeFilter


class DevelopmentPlanViewSet(viewsets.ModelViewSet):
    queryset = DevelopmentPlan.objects.all()
    serializer_class = DevelopmentPlanSerializer

class MetricViewSet(viewsets.ViewSet):
    def create(self, request, metric_type):
        request_serializer = MetricRequestSerializer(data=request.data)

        # Получаем команду с id=1
        try:
            user = ManagerTeam.objects.get(pk=1)
            print(user)
        except ManagerTeam.DoesNotExist:
            return Response({"error": "ManagerTeam with id=1 does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if request_serializer.is_valid():
            start_period = request_serializer.validated_data['startPeriod']
            end_period = request_serializer.validated_data['endPeriod']

            # Получаем всех сотрудников команды с id=1
            team_employees = EmployeeTeam.objects.filter(manager=user).values_list('employee', flat=True)
            print(team_employees)

            dashboard = []
            total_performance = 0
            employee_count = 0

            # Определяем модель в зависимости от типа метрики
            model = None
            if metric_type == 'development_plan':
                model = EmployeeDevelopmentPlan
            elif metric_type == 'engagement':
                model = EmployeeEngagement
            elif metric_type == 'employees':
                return self.get_employee_data(team_employees, start_period, end_period)
            else:
                return Response(
                    {"error": "Invalid metric type."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Обрабатываем данные по каждому сотруднику команды
            for employee_id in team_employees:
                try:
                    # Получаем данные только за указанный период
                    employee_metrics = model.objects.filter(
                        employee=employee_id,
                        add_date__range=(start_period, end_period)  # Фильтрация по полю add_date
                    )
                    print(employee_metrics)
                    if employee_metrics.exists():
                        # Считаем среднее значение за период для данного сотрудника
                        employee_performance = employee_metrics.aggregate(
                            avg_performance=Avg('development_progress' if metric_type == 'development_plan' else 'engagement_level')
                        )
                        avg_performance = employee_performance['avg_performance'] or 0

                        dashboard.append({
                            "employee": employee_id,  # Заменяем employee на employee_id
                            "period": {
                                "start": start_period,
                                "end": end_period
                            },
                            "performance": str(avg_performance)
                        })

                        total_performance += avg_performance
                        employee_count += 1
                except model.DoesNotExist:
                    continue

            # Среднее значение производительности за период для всех сотрудников
            avg_performance_for_all = total_performance / employee_count if employee_count else 0

            response_data = {
                "dashboard": dashboard,
                "averagePerformanceForAll": str(avg_performance_for_all)
            }

            return Response(response_data, status=status.HTTP_200_OK)

        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_employee_data(self, team_employees, start_period, end_period):
        """ Логика получения данных по количеству сотрудников. """
        dashboard = []

        # Получаем общие данные, без необходимости перебора всех сотрудников
        number_of_employees = Employee.objects.count()
        number_of_bus_factors = BusFactor.objects.count()
        number_of_key_people = Employee.objects.filter(is_key_person=True).count()

        dashboard.append({
            "period": {
                "start": start_period,
                "end": end_period
            },
            "countData": [
                {
                    "numberOfEmployees": str(number_of_employees),
                    "numberOfBusFactors": str(number_of_bus_factors),
                    "numberOfKeyPeople": str(number_of_key_people)
                }
            ]
        })

        return Response({"count": dashboard}, status=status.HTTP_200_OK)



