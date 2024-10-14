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
    EmployeeSerializer,
    # DevelopmentPlanSerializer,
    TimePeriodRequestSerializer,
    TeamMetricsResponseSerializer,
    SkillAssessmentRequestSerializer,
    TeamMetricsRequestSerializer, 
    SkillDomenRequestSerializer, 
    MetricResponseSerializer,
    CompetencyLevelRequestSerializer,
    EmployeeCompetencySerializer,
    TeamMetricResponseSerializer, 
    TeamEmployeeDashboardSerializer,
    CompetencySerializer   
)

from rest_framework.response import Response
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from datetime import datetime
from calendar import month_name
from django.db.models import Sum
# class EmployeesViewSet(viewsets.ModelViewSet):
#     serializer_class = EmployeeSerializer

#     def get_queryset(self):
#         team_slug = self.kwargs.get('team_slug')  # Получаем слаг команды
#         user = self.request.user

#         # Получаем команду или возвращаем 404, если она не найдена
#         team = get_object_or_404(Team, slug=team_slug)

#         # Получаем менеджера или возвращаем 404, если он не найден
#         manager = get_object_or_404(ManagerTeam, email=user.email)

#         # Возвращаем сотрудников, относящихся к команде текущего менеджера
#         return Employee.objects.filter(
#             teams__team=team,  # Используем ManyToMany связь
#             teams__manager=manager  # Фильтруем по менеджеру
#         )


class DateConversionMixin:
    def convert_to_date(self, start_period, end_period):
        start_date = datetime.strptime(f"{start_period['year']}-{start_period['month']}-15", "%Y-%B-%d").date()
        end_date = datetime.strptime(f"{end_period['year']}-{end_period['month']}-15", "%Y-%B-%d").date()
        return start_date, end_date


class EmployeesViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        team_slug = self.kwargs.get('team_slug')
        team = get_object_or_404(Team, slug=team_slug)
        manager = get_object_or_404(ManagerTeam, id=2)

        return Employee.objects.filter(teams__team=team, teams__manager=manager)



class MetricViewSet(DateConversionMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = TimePeriodRequestSerializer

    def create(self, request, metric_type, employee_id):
        # Используем встроенный метод для валидации данных через сериализатор
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            return self.error_response(serializer.errors)

        start_date, end_date = self.convert_to_date(
            serializer.validated_data['startPeriod'],
            serializer.validated_data['endPeriod']
        )

        model = self.get_metric_model(metric_type)
        if model is None:
            return self.error_response({"error": "Invalid metric type."})

        dashboard, last_performance = self.get_employee_metrics(employee_id, model, start_date, end_date)
        response_data = {
            "dashboard": dashboard,
            "completionForToday": last_performance
        }

        return Response(response_data, status=status.HTTP_200_OK)

    
    def get_employee_metrics(self, employee_id, model, start_date, end_date):
        employee_metrics = model.objects.filter(employee__id=employee_id, add_date__range=[start_date, end_date])

        if not employee_metrics.exists():
            return [], "0.00"

        metrics_by_month = self.group_metrics_by_month(employee_metrics)
        dashboard = [
            {
                "period": {"month": month_name[month], "year": year},
                "performance": str(performance)
            }
            for (year, month), performance in metrics_by_month.items()
        ]

        last_performance = dashboard[-1]['performance'] if dashboard else "0.00"
        return dashboard, last_performance

    def group_metrics_by_month(self, employee_metrics):
        metrics_by_month = {}
        for metric in employee_metrics:
            key = (metric.add_date.year, metric.add_date.month)
            metrics_by_month[key] = metrics_by_month.get(key, 0) + metric.performance_score
        return metrics_by_month

    def get_metric_model(self, metric_type):
        return {
            'development_plan': EmployeeDevelopmentPlan,
            'involvement': EmployeeEngagement
        }.get(metric_type)

    def method_not_allowed_response(self):
        return Response({"error": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def error_response(self, errors):
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class TeamCountEmployeeViewSet(DateConversionMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    
    serializer_class = TimePeriodRequestSerializer

    def create(self, request, team_slug):
        if request.method != 'POST':
            return self.method_not_allowed_response()

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            start_date, end_date = self.convert_to_date(
                serializer.validated_data['startPeriod'],
                serializer.validated_data['endPeriod']
            )
            return self.get_team_employee_data(team_slug, start_date, end_date)

        return self.error_response(serializer.errors)

    def get_team_employee_data(self, team_slug, start_date, end_date):
        team = get_object_or_404(EmployeeTeam, team__slug=team_slug)
        employees = team.employee.all()

        number_of_employees = employees.count()
        number_of_bus_factors = EmployeeBusFactor.objects.filter(
            employee__in=employees, add_date__range=[start_date, end_date]
        ).count()
        number_of_key_people = EmployeeKeyPeople.objects.filter(
            employee__in=employees, add_date__range=[start_date, end_date]
        ).count()

        dashboard_data = {
            "period": {"month": month_name[start_date.month], "year": str(start_date.year)},
            "numberOfEmployee": str(number_of_employees),
            "numberOfBusFactor": str(number_of_bus_factors),
            "numberOfKeyPeople": str(number_of_key_people)
        }

        response_serializer = TeamEmployeeDashboardSerializer(data=dashboard_data)
        if response_serializer.is_valid():
            return Response({"dashboard": [response_serializer.data]}, status=status.HTTP_200_OK)

        return self.error_response(response_serializer.errors)


class TeamMetricViewSet(DateConversionMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = TimePeriodRequestSerializer
    def create(self, request, team_slug, metric_type):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return self.error_response(serializer.errors)

        start_date, end_date = self.convert_to_date(
            serializer.validated_data['startPeriod'],
            serializer.validated_data['endPeriod']
        )

        team = get_object_or_404(EmployeeTeam, team__slug=team_slug)
        employees = team.employee.all()
        model = self.get_metric_model(metric_type)

        if model is None:
            return self.error_response({"error": "Invalid metric type."})

        metrics_by_month = self.get_metrics_by_month(employees, model, start_date, end_date)

        dashboard_data = [
            {"period": {"year": year, "month": month_name[month]}, "performance": str(performance / len(employees))}
            for (year, month), performance in metrics_by_month.items()
        ]

        completion_for_today = dashboard_data[-1]['performance'] if dashboard_data else "0.00"
        response_data = {
            "dashboard": dashboard_data,
            "completionForToday": completion_for_today
        }

        response_serializer = TeamMetricResponseSerializer(data=response_data)
        if response_serializer.is_valid():
            return Response(response_serializer.data, status=status.HTTP_200_OK)

        return self.error_response(response_serializer.errors)

    def get_metric_model(self, metric_type):
        return {
            'development_plan': EmployeeDevelopmentPlan,
            'involvement': EmployeeEngagement
        }.get(metric_type)
    
    def get_metrics_by_month(self, employees, model, start_date, end_date):
        metrics_by_month = {}
        for employee in employees:
            for metric in model.objects.filter(employee=employee, add_date__range=[start_date, end_date]):
                key = (metric.add_date.year, metric.add_date.month)
                metrics_by_month[key] = metrics_by_month.get(key, 0) + metric.performance_score
        return metrics_by_month


class TeamIndividualCompetenciesViewSet(DateConversionMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SkillDomenRequestSerializer
    
    def create(self, request, team_slug, employee_id=None):
        if request.method != 'POST':
            return self.method_not_allowed_response()

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            skill_domen = serializer.validated_data['skillDomen']
            team = get_object_or_404(EmployeeTeam, team__slug=team_slug)

            competencies = self.get_competencies(team, employee_id, skill_domen)

            response_serializer = CompetencySerializer(competencies, many=True, context={'skill_domen': skill_domen})
            return Response({"data": response_serializer.data}, status=status.HTTP_200_OK)

        return self.error_response(serializer.errors)

    def get_competencies(self, team, employee_id, skill_domen):
        filter_kwargs = {
            'employee__teams': team,
            'competency__competency_type': skill_domen
        }
        if employee_id is not None:
            filter_kwargs['employee__id'] = employee_id

        return EmployeeCompetency.objects.filter(**filter_kwargs)


class CompetencyLevelViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = CompetencyLevelRequestSerializer
    
    def create(self, request, team_slug, employee_id=None):
        if request.method != 'POST':
            return self.method_not_allowed_response()

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return self.error_response(serializer.errors)

        competency_id = serializer.validated_data['competencyId']
        team = get_object_or_404(EmployeeTeam, team__slug=team_slug)

        employees = self.get_employees(team, employee_id)

        employee_competencies = EmployeeCompetency.objects.filter(
            employee__in=employees,
            competency__id=competency_id,
        )

        serializer = EmployeeCompetencySerializer(employee_competencies, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def get_employees(self, team, employee_id):
        return team.employee.filter(id=employee_id) if employee_id else team.employee.all()

    def method_not_allowed_response(self):
        return Response({"error": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def error_response(self, errors):
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
#################################


class SkillAssessmentViewSet(viewsets.ViewSet):
    """
    ViewSet для получения оценки навыков команды и индивидуальных навыков.
    """

    def create(self, request, *args, **kwargs):
        # Получаем URL, чтобы понять какой тип оценки запрашивается
        if 'team-skill-assessment' in request.path:
            return self.team_skill_assessment(request)
        elif 'individual-skill-assessment' in request.path:
            return self.individual_skill_assessment(request)
        else:
            return Response({"detail": "Invalid URL"}, status=status.HTTP_404_NOT_FOUND)

    def team_skill_assessment(self, request):
        """
        Получение оценки навыков команды.
        """
        # Десериализация тела запроса
        serializer = SkillAssessmentRequestSerializer(data=request.data)
        if serializer.is_valid():
            employee_ids = serializer.validated_data['employeeIds']
            skill_domen = serializer.validated_data['skillDomen']
            start_period = serializer.validated_data['startPeriod']
            end_period = serializer.validated_data['endPeriod']

            # Логика для получения оценки навыков команды
            skills_data = []
            for skill in Skill.objects.filter(domen=skill_domen):
                # Фильтруем данные по навыкам, сотрудникам и периодам
                skill_assessments = EmployeeSkill.objects.filter(
                    employee__in=employee_ids,
                    skill=skill,
                    period__month__gte=start_period['month'],
                    period__year__gte=start_period['year'],
                    period__month__lte=end_period['month'],
                    period__year__lte=end_period['year']
                )

                # Рассчитываем среднюю оценку по всем сотрудникам для конкретного навыка
                avg_assessment = skill_assessments.aggregate(average=Avg('assesment'))['average']
                if avg_assessment:
                    skills_data.append({
                        'skillId': skill.id,
                        'skillName': skill.name,
                        'assesment': avg_assessment
                    })

            # Формирование ответа
            response_data = [
                {
                    "period": start_period,  # Здесь можно использовать цикл для каждого месяца в периоде
                    "skillsData": skills_data
                }
            ]
            return Response({"data": response_data}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def individual_skill_assessment(self, request):
        """
        Получение оценки навыков сотрудника.
        """
        # Десериализация тела запроса
        serializer = SkillAssessmentRequestSerializer(data=request.data)
        if serializer.is_valid():
            employee_id = serializer.validated_data['employeeIds'][0]  # Ожидаем одного сотрудника
            skill_domen = serializer.validated_data['skillDomen']
            start_period = serializer.validated_data['startPeriod']
            end_period = serializer.validated_data['endPeriod']

            # Логика для получения оценки навыков сотрудника
            skills_data = []
            for skill in Skill.objects.filter(domen=skill_domen):
                # Фильтруем данные по навыкам и сотруднику
                skill_assessments = EmployeeSkill.objects.filter(
                    employee_id=employee_id,
                    skill=skill,
                    period__month__gte=start_period['month'],
                    period__year__gte=start_period['year'],
                    period__month__lte=end_period['month'],
                    period__year__lte=end_period['year']
                )

                # Рассчитываем среднюю оценку сотрудника для конкретного навыка
                avg_assessment = skill_assessments.aggregate(average=Avg('assesment'))['average']
                if avg_assessment:
                    skills_data.append({
                        'skillId': skill.id,
                        'skillName': skill.name,
                        'assesment': avg_assessment
                    })

            # Формирование ответа
            response_data = [
                {
                    "period": start_period,  # Здесь можно использовать цикл для каждого месяца в периоде
                    "skillsData": skills_data
                }
            ]
            return Response({"data": response_data}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
 
 
        
        
# НАДО БУДЕТСДЕЛАТЬ ЧТОБЫ ВОЗВРАТ БЫЛ НЕ return Response({"data": response_data} А ЧЕРЕЗ СЕРИАЛИЗАТОР ВО ВСЕХ ВЬЮ 