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
    IndividualDevelopmentPlanRequestSerializer,
    TeamMetricsResponseSerializer,
    SkillAssessmentRequestSerializer,
    TeamMetricsRequestSerializer, 
    SkillDomenRequestSerializer, 
    MetricResponseSerializer,
    CompetencyLevelRequestSerializer   
)

from rest_framework.response import Response
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from datetime import datetime
from calendar import month_name


class EmployeesViewSet(viewsets.ModelViewSet): 
    serializer_class = EmployeeSerializer
    
    def get_queryset(self):
        team_slug = self.kwargs.get('team_slug')  # Получаем слаг команды
        print(team_slug)
        # user = self.request.user
        # user = ManagerTeam.objects.get(id=1)
        
        team = Team.objects.get(slug=team_slug)  # Предполагается, что у команды есть связь с slug
        manager = ManagerTeam.objects.get(id=1)  # Предполагается, что у менеджера есть связь с пользователем

        # Возвращаем сотрудников, относящихся к команде текущего менеджера
        return Employee.objects.filter(
            teams__team=team,  # Используем ManyToMany связь
            teams__manager=manager  # Фильтруем по менеджеру
        )


class MetricViewSet(viewsets.ViewSet):
    serializer_class = TeamMetricsResponseSerializer
    def create(self, request, metric_type):
        if request.method != 'POST':
            return Response({"error": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        serializer = IndividualDevelopmentPlanRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        employee_ids = serializer.validated_data['employeeIds']
        start_date, end_date = self.convert_to_date(
            serializer.validated_data['startPeriod'], 
            serializer.validated_data['endPeriod']
        )

        # Определяем модель по метрике
        model = {
            'development_plan': EmployeeDevelopmentPlan,
            'involvement': EmployeeEngagement
        }.get(metric_type)

        if not model:
            return Response({"error": "Invalid metric type."}, status=status.HTTP_400_BAD_REQUEST)

        dashboard, last_performance = self.get_employee_metrics(employee_ids, model, start_date, end_date)

        response_data = {
            "dashboard": [],
            "completionForToday": last_performance
        }

        for entry in dashboard:
            metric_serializer = MetricResponseSerializer(data=entry)
            if metric_serializer.is_valid():
                response_data["dashboard"].append(metric_serializer.data)

        return Response(response_data, status=status.HTTP_200_OK)

    def get_employee_metrics(self, employee_ids, model, start_date, end_date):
        dashboard = []

        for employee_id in employee_ids:
            employee_metrics = model.objects.filter(
                employee__employee_id=employee_id,
                add_date__range=[start_date, end_date]
            )

            if not employee_metrics.exists():
                continue

            # Группируем метрики по месяцам
            metrics_by_month = self.group_metrics_by_month(employee_metrics)

            for (year, month), performance in metrics_by_month.items():
                dashboard.append({
                    "period": {"month": month_name[month], "year": year},
                    "performance": str(performance)
                })

        last_performance = dashboard[-1]['performance'] if dashboard else "0.00"
        return dashboard, last_performance

    def group_metrics_by_month(self, employee_metrics):
        metrics_by_month = {}
        for metric in employee_metrics:
            key = (metric.add_date.year, metric.add_date.month)
            metrics_by_month[key] = metrics_by_month.get(key, 0) + metric.performance_score
        return metrics_by_month

    def convert_to_date(self, start_period, end_period):
        start_date = datetime.strptime(f"{start_period['year']}-{start_period['month']}-09", "%Y-%B-%d").date()
        end_date = datetime.strptime(f"{end_period['year']}-{end_period['month']}-09", "%Y-%B-%d").date()
        return start_date, end_date


class TeamCountEmployeeViewSet(viewsets.ViewSet):
    def create(self, request, team_slug):
        if request.method != 'POST':
            return Response({"error": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        request_serializer = TeamMetricsRequestSerializer(data=request.data)

        if request_serializer.is_valid():
            start_period = request_serializer.validated_data['startPeriod']
            end_period = request_serializer.validated_data['endPeriod']

            return self.get_team_employee_data(team_slug, start_period, end_period)

        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_team_employee_data(self, team_slug, start_period, end_period):
        dashboard = []

        # Получаем команду по слагу
        try:
            team = EmployeeTeam.objects.get(team__slug=team_slug)
            employees = team.employee.all()  # Получаем всех сотрудников команды

            # Преобразуем даты начала и окончания
            start_date, end_date = self.convert_to_date(start_period, end_period)

            # Получаем количество сотрудников, Bus факторов и Key People
            number_of_employees = employees.count()
            number_of_bus_factors = EmployeeBusFactor.objects.filter(
                employee__in=employees,
                add_date__range=[start_date, end_date]
            ).count()
            number_of_key_people = EmployeeKeyPeople.objects.filter(
                employee__in=employees,
                add_date__range=[start_date, end_date]
            ).count()

            # Добавляем результаты в dashboard
            dashboard.append({
                "period": {
                    "month": month_name[start_date.month],
                    "year": str(start_date.year)
                },
                "numberOfEmployee": str(number_of_employees),
                "numberOfBusFactor": str(number_of_bus_factors),
                "numberOfKeyPeople": str(number_of_key_people)
            })

            return Response({"dashboard": dashboard}, status=status.HTTP_200_OK)

        except EmployeeTeam.DoesNotExist:
            return Response({"error": "Team not found."}, status=status.HTTP_404_NOT_FOUND)

    def convert_to_date(self, start_period, end_period):
        start_date = datetime.strptime(f"{start_period['year']}-{start_period['month']}-09", "%Y-%B-%d").date()
        end_date = datetime.strptime(f"{end_period['year']}-{end_period['month']}-09", "%Y-%B-%d").date()
        return start_date, end_date


#################################
class TeamMetricViewSet(viewsets.ViewSet):
    def create(self, request, team_slug, metric_type):
        request_serializer = TeamMetricsRequestSerializer(data=request.data)
        if not request_serializer.is_valid():
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        start_date, end_date = self.convert_to_date(
            request_serializer.validated_data['startPeriod'],
            request_serializer.validated_data['endPeriod']
        )

        try:
            employees = EmployeeTeam.objects.get(team__slug=team_slug).employee.all()
        except EmployeeTeam.DoesNotExist:
            return Response({"error": "Team not found."}, status=status.HTTP_404_NOT_FOUND)

        model = self.get_metric_model(metric_type)
        if model is None:
            return Response({"error": "Invalid metric type."}, status=status.HTTP_400_BAD_REQUEST)

        metrics_by_month = {}
        for employee in employees:
            for metric in model.objects.filter(employee=employee, add_date__range=[start_date, end_date]):
                key = (metric.add_date.year, metric.add_date.month)
                metrics_by_month[key] = metrics_by_month.get(key, 0) + metric.performance_score

        dashboard = [
            {"period": {"month": month_name[month], "year": year}, "performance": str(performance / len(employees))}
            for (year, month), performance in metrics_by_month.items()
        ]

        completion_for_today = dashboard[-1]['performance'] if dashboard else "0.00"

        # Формируем ответ через сериализатор
        response_data = {
            "dashboard": [],
            "completionForToday": completion_for_today
        }

        for entry in dashboard:
            metric_serializer = MetricResponseSerializer(data=entry)
            if metric_serializer.is_valid():
                response_data["dashboard"].append(metric_serializer.data)

        return Response(response_data, status=status.HTTP_200_OK)

    def convert_to_date(self, start_period, end_period):
        return (datetime.strptime(f"{start_period['year']}-{start_period['month']}-09", "%Y-%B-%d").date(),
                datetime.strptime(f"{end_period['year']}-{end_period['month']}-09", "%Y-%B-%d").date())

    def get_metric_model(self, metric_type):
        return {
            'development_plan': EmployeeDevelopmentPlan,
            'involvement': EmployeeEngagement
        }.get(metric_type)


class TeamIndividualCompetenciesViewSet(viewsets.ViewSet):
    def create(self, request, team_slug, employee_id=None):
        if request.method != 'POST':
            return Response({"error": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        request_serializer = SkillDomenRequestSerializer(data=request.data)

        if request_serializer.is_valid():
            skill_domen = request_serializer.validated_data['skillDomen']
            team = get_object_or_404(EmployeeTeam, team__slug=team_slug)

            competencies = self.get_competencies(team, employee_id, skill_domen)
            data = self.prepare_competency_data(competencies, skill_domen)

            # Возвращаем данные в формате {"data": data}
            return Response({"data": data}, status=status.HTTP_200_OK)

        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_competencies(self, team, employee_id, skill_domen):
        if employee_id is not None:
            employee = get_object_or_404(team.employee.all(), id=employee_id)
            return EmployeeCompetency.objects.filter(
                employee=employee,
                competency__competency_type=skill_domen
            )
        else:
            return EmployeeCompetency.objects.filter(
                employee__in=team.employee.all(),
                competency__competency_type=skill_domen
            )

    def prepare_competency_data(self, competencies, skill_domen):
        data = []
        for competency in competencies:
            data.append({
                "competencyId": competency.competency.id,
                "skillDomen": skill_domen.capitalize(),
                "competencyName": competency.competency.competency_name,
                "plannedResult": str(competency.planned_result),
                "actualResult": f"{competency.actual_result:.1f}"
            })
        return data


class CompetencyLevelViewSet(viewsets.ViewSet):
    """
    ViewSet для получения уровня компетенций сотрудников.
    """

    def create(self, request, team_slug, employee_id=None):
        if request.method != 'POST':
            return Response({"error": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        # Валидация данных запроса
        request_serializer = CompetencyLevelRequestSerializer(data=request.data)
        if not request_serializer.is_valid():
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Получаем данные из запроса
        competency_id = request_serializer.validated_data['competencyId']
        team = get_object_or_404(EmployeeTeam, team__slug=team_slug)

        # Получаем сотрудников команды
        employees = self.get_employees(team, employee_id)

        # Фильтруем компетенции сотрудников
        employee_competencies = EmployeeCompetency.objects.filter(
            employee__in=employees,
            competency__id=competency_id,
        )

        # Если компетенций нет
        if not employee_competencies.exists():
            return Response({"data": []}, status=status.HTTP_200_OK)

        # Формируем данные для ответа
        data = self.prepare_competency_data(employee_competencies)
        return Response({"data": data}, status=status.HTTP_200_OK)

    def get_employees(self, team, employee_id):
        """Получаем сотрудников команды, фильтруя по employee_id, если передан."""
        return team.employee.filter(id=employee_id) if employee_id else team.employee.all()

    def prepare_competency_data(self, employee_competencies):
        """Подготавливаем данные для ответа."""
        data = []
        for emp_competency in employee_competencies:
            data.append({
                "employeeId": emp_competency.employee.id,
                "skillDomen": emp_competency.competency.competency_type.capitalize(),
                "assessment": str(emp_competency.competency_level),
                "color": self.get_color_based_on_assessment(emp_competency.competency_level)
            })
        return data

    def get_color_based_on_assessment(self, competency_level):
        """
        Метод для определения цвета в зависимости от уровня компетенции.
        """
        level = int(competency_level)
        if level > 80:
            return "green"
        elif level >= 60:
            return "yellow"
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