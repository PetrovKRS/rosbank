
from calendar import month_name
from datetime import datetime, date
from typing import Optional, Tuple, List, Dict

from django.db.models import Avg, Sum, QuerySet
from django.db.models.functions import ExtractMonth, ExtractYear
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import (
    mixins,
    status,
    viewsets,
)

from core.models import (
    EmployeeDevelopmentPlan,
    EmployeeEngagement,
    EmployeeKeyPeople,
    EmployeeBusFactor,
    Team,
    EmployeeTeam,
    EmployeeCompetency,
    EmployeeSkill,
    ManagerTeam,
    Employee,
)
from api.serializers import (
    SkillSerializer,
    CompetencySerializer,
    TeamSkillSerializer,
    EmployeeSerializer,
    TimePeriodRequestSerializer,
    SkillDomenRequestSerializer,
    CompetencyLevelRequestSerializer,
    EmployeeCompetencySerializer,
    TeamMetricResponseSerializer,
    SkillLevelRequestSerializer,
    TeamEmployeeDashboardSerializer,
)
from api.filters import EmployeeFilter


class DateConversionMixin:
    def convert_to_date(
        self, start_period: dict, end_period: dict
    ) -> Tuple[date, date]:
        """
        Преобразует периоды (начальный и конечный) в объекты даты.
        Параметры:
        - start_period (dict): Словарь с ключами 'year' (строка) и 'month' (название месяца на английском).
        - end_period (dict): Словарь с ключами 'year' (строка) и 'month' (название месяца на английском).
        Возвращает:
        - Tuple[date, date]: Кортеж с двумя объектами `date` — начальной и конечной датами.
        """
        start_date = datetime.strptime(
            f"{start_period['year']}-{start_period['month']}-18", "%Y-%B-%d"
        ).date()
        end_date = datetime.strptime(
            f"{end_period['year']}-{end_period['month']}-18", "%Y-%B-%d"
        ).date()
        return start_date, end_date


class EmployeesViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    Обрабатывает запросы для получения списка сотрудников и отдельного сотрудника.
    """

    serializer_class = EmployeeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = EmployeeFilter

    def get_queryset(self) -> QuerySet[Employee]:
        """
        Получает набор сотрудников, относящихся к конкретной команде и менеджеру.
        """
        team_slug = self.kwargs.get('team_slug')
        team = get_object_or_404(Team, slug=team_slug)
        manager = get_object_or_404(ManagerTeam, id=2)

        return Employee.objects.filter(
            teams__team=team, teams__manager=manager
        )


class MetricViewSet(
    DateConversionMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    """
    Обрабатывает запросы для создания метрик по заданным временным периодам.
    """

    serializer_class = TimePeriodRequestSerializer

    def create(self, request, metric_type: str, employee_id: int) -> Response:
        """
        Создает метрики для сотрудника на основе временного периода.
        Параметры:
        - request: объект запроса.
        - metric_type: тип метрики.
        - employee_id: идентификатор сотрудника.
        Возвращает:
        - Response: данные метрик и статус 200 (OK).
        """
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return self.error_response(serializer.errors)

        start_date, end_date = self.convert_to_date(
            serializer.validated_data['startPeriod'],
            serializer.validated_data['endPeriod'],
        )

        model = self.get_metric_model(metric_type)
        if model is None:
            return self.error_response({"error": "Invalid metric type."})

        dashboard, last_performance = self.get_employee_metrics(
            employee_id, model, start_date, end_date
        )
        response_data = {
            "dashboard": dashboard,
            "completionForToday": last_performance,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def get_employee_metrics(
        self, employee_id: int, model: str, start_date: date, end_date: date
    ) -> Tuple[List[dict], str]:
        """
        Получает метрики сотрудника за заданный период.
        Параметры:
        - employee_id: идентификатор сотрудника.
        - model: модель метрики.
        - start_date: дата начала периода.
        - end_date: дата окончания периода.
        Возвращает:
        - dashboard: список метрик по месяцам.
        - last_performance: последняя метрика производительности.
        """
        employee_metrics = model.objects.filter(
            employee__id=employee_id, add_date__range=[start_date, end_date]
        )

        if not employee_metrics.exists():
            return [], "0.00"

        metrics_by_month = self.group_metrics_by_month(employee_metrics)
        dashboard = [
            {
                "period": {"month": month_name[month], "year": year},
                "performance": str(performance),
            }
            for (year, month), performance in metrics_by_month.items()
        ]

        last_performance = (
            dashboard[-1]['performance'] if dashboard else "0.00"
        )
        return dashboard, last_performance

    def group_metrics_by_month(
        self, employee_metrics: QuerySet
    ) -> Dict[Tuple[int, int], float]:
        """
        Группирует метрики по месяцу и вычисляет среднее значение performance_score.
        Параметры:
        - employee_metrics: метрики сотрудника.
        Возвращает:
        - metrics_by_month_dict: словарь с ключом (year, month) и значением среднего performance_score.
        """
        metrics_by_month = (
            employee_metrics.annotate(
                year=ExtractYear('add_date'), month=ExtractMonth('add_date')
            )
            .values('year', 'month')
            .annotate(average_performance=Avg('performance_score'))
            .order_by('year', 'month')
        )

        metrics_by_month_dict = {
            (metric['year'], metric['month']): round(
                metric['average_performance'], 2
            )
            for metric in metrics_by_month
        }

        return metrics_by_month_dict

    def get_metric_model(self, metric_type: str):
        """
        Получает модель метрики по типу.
        """
        return {
            'development_plan': EmployeeDevelopmentPlan,
            'involvement': EmployeeEngagement,
        }.get(metric_type)

    def method_not_allowed_response(self) -> Response:
        """
        Возвращает ответ с ошибкой 405 (Method Not Allowed).
        """
        return Response(
            {"error": "Method not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def error_response(self, errors: dict) -> Response:
        """
        Возвращает ответ с ошибками валидации.
        """
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class TeamCountEmployeeViewSet(
    DateConversionMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    serializer_class = TimePeriodRequestSerializer

    def create(self, request, team_slug):
        if request.method != 'POST':
            return self.method_not_allowed_response()

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if 'startPeriod' in serializer.validated_data:
                start_date, end_date = self.convert_to_date(
                    serializer.validated_data['startPeriod'],
                    serializer.validated_data['endPeriod']
                )
                return self.get_team_employee_data(team_slug, start_date, end_date)
            else:
                return self.get_team_employee_data(team_slug)

    def get_team_employee_data(self, team_slug, start_date=None, end_date=None):
        team = get_object_or_404(EmployeeTeam, team__slug=team_slug)
        employees = team.employee.all()

        number_of_employees = employees.count()
        period = {}
        if start_date and end_date:
            number_of_bus_factors = EmployeeBusFactor.objects.filter(
                employee__in=employees, add_date__range=[start_date, end_date]
            ).count()
            number_of_key_people = EmployeeKeyPeople.objects.filter(
                employee__in=employees, add_date__range=[start_date, end_date]
            ).count()
            period = {

                "startDate":{
                        "month": month_name[start_date.month],
                        "year": str(start_date.year),
                },
                "endDate":{
                    "month": month_name[end_date.month],
                    "year": str(end_date.year),
                }
            }
        else:
            number_of_bus_factors = EmployeeBusFactor.objects.filter(
                employee__in=employees
            ).count()
            number_of_key_people = EmployeeKeyPeople.objects.filter(
                employee__in=employees
            ).count()

        dashboard_data = {
            "period": period,
            "numberOfEmployee": str(number_of_employees),
            "numberOfBusFactor": str(number_of_bus_factors),
            "numberOfKeyPeople": str(number_of_key_people)
        }

        response_serializer = TeamEmployeeDashboardSerializer(data=dashboard_data)
        if response_serializer.is_valid():
            return Response(dashboard_data, status=status.HTTP_200_OK)

        return self.error_response(response_serializer.errors)

    def error_response(self, errors):
        """Метод для обработки ошибок сериализатора."""
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def method_not_allowed_response(self):
        """Метод для обработки неподдерживаемых методов."""
        return Response(
            {"error": "Method not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


class TeamMetricViewSet(
    DateConversionMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    """
    Обрабатывает запросы для получения метрик по команде за заданный временной период.
    """

    serializer_class = TimePeriodRequestSerializer

    def create(self, request, team_slug: str, metric_type: str) -> Response:
        """
        Создает метрики для команды на основе временного периода.
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return self.error_response(serializer.errors)

        start_date, end_date = self.convert_to_date(
            serializer.validated_data['startPeriod'],
            serializer.validated_data['endPeriod'],
        )

        team = get_object_or_404(EmployeeTeam, team__slug=team_slug)
        employees = team.employee.all()
        model = self.get_metric_model(metric_type)

        if model is None:
            return self.error_response({"error": "Invalid metric type."})

        metrics_by_month = self.get_metrics_by_month(
            employees, model, start_date, end_date
        )

        dashboard_data = [
            {
                "period": {"year": year, "month": month_name[month]},
                "performance": str(round(performance / len(employees), 2)),
            }
            for (year, month), performance in metrics_by_month.items()
        ]

        completion_for_today = (
            dashboard_data[-1]['performance'] if dashboard_data else "0.00"
        )
        response_data = {
            "dashboard": dashboard_data,
            "completionForToday": completion_for_today,
        }

        response_serializer = TeamMetricResponseSerializer(data=response_data)
        if response_serializer.is_valid():
            return Response(
                response_serializer.data, status=status.HTTP_200_OK
            )

        return self.error_response(response_serializer.errors)

    def get_metric_model(self, metric_type: str):
        """
        Получает модель метрики на основе типа.
        """
        return {
            'development_plan': EmployeeDevelopmentPlan,
            'involvement': EmployeeEngagement,
        }.get(metric_type)

    def get_metrics_by_month(
        self, employees, model, start_date: str, end_date: str
    ) -> Dict[tuple, float]:
        """
        Получает метрики сотрудников по месяцам.
        """
        metrics_by_month = (
            model.objects.filter(
                employee__in=employees, add_date__range=[start_date, end_date]
            )
            .annotate(
                year=ExtractYear('add_date'), month=ExtractMonth('add_date')
            )
            .values('year', 'month')
            .annotate(total_performance=Sum('performance_score'))
            .order_by('year', 'month')
        )

        metrics_by_month_dict = {
            (metric['year'], metric['month']): metric['total_performance']
            for metric in metrics_by_month
        }
        return metrics_by_month_dict


class TeamIndividualCompetenciesViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """ViewSet для получения значений оценки компетенции сотрудника/команды."""

    def create(self, request, team_slug, employee_id=None):
        """Создает запрос на получение значений оценки компетенции сотрудников в команде."""
        if request.method != 'POST':
            return self.method_not_allowed_response()

        if 'employeeIds' in self.request.data:
            employee_id = self.request.data.get('employeeIds')

        request_serializer = SkillDomenRequestSerializer(data=request.data)

        if request_serializer.is_valid():
            skill_domen = request_serializer.validated_data['skillDomen']
            team = get_object_or_404(EmployeeTeam, team__slug=team_slug)

            competencies = self.get_competencies(team, employee_id, skill_domen)
            data = self.prepare_competency_data(competencies, skill_domen)

            return Response({"data": data}, status=status.HTTP_200_OK)

        return self.error_response(request_serializer.errors)

    def get_competencies(self, team, employee_id, skill_domen):
        """Получаем компетенции команды, фильтруя по employee_id, если передан."""
        if employee_id is not None:
            return EmployeeCompetency.objects.filter(
                employee__id__in=employee_id,
                employee__teams=team,
                competency__competency_type=skill_domen,
            )
        else:
            return EmployeeCompetency.objects.filter(
                employee__teams=team, competency__competency_type=skill_domen
            )

    def prepare_competency_data(self, competencies, skill_domen):
        """Подготавливаем данные для ответа."""
        data = []
        for competency in competencies:
            planned_avg = (
                EmployeeCompetency.objects.filter(
                    competency__id=competency.competency.id
                ).aggregate(Avg('planned_result'))['planned_result__avg'] or 0
            )

            actual_avg = (
                EmployeeCompetency.objects.filter(
                    competency__id=competency.competency.id
                ).aggregate(Avg('actual_result'))['actual_result__avg'] or 0
            )

            temp = {
                "competencyId": competency.competency.id,
                "skillDomen": skill_domen.capitalize(),
                "competencyName": competency.competency.competency_name,
                "plannedResult": round(planned_avg, 2),
                "actualResult": round(actual_avg, 2),
            }
            if not any(d['competencyId'] == temp['competencyId'] for d in data):
                data.append(temp)

        serializer = CompetencySerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)

        return serializer.data

    def method_not_allowed_response(self):
        """Метод для обработки неподдерживаемых методов."""
        return Response(
            {"error": "Method not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def error_response(self, errors):
        """Метод для обработки ошибок валидации."""
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class CompetencyLevelViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Обрабатывает запросы для получения уровней компетенций сотрудников.
    """

    serializer_class = CompetencyLevelRequestSerializer

    def create(
        self, request, team_slug: str, employee_id: Optional[int] = None
    ) -> Response:
        """
        Создает запрос на получение уровней компетенций для сотрудников в команде.
        """

        if request.method != 'POST':
            return self.method_not_allowed_response()

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return self.error_response(serializer.errors)

        competency_id = serializer.validated_data['competencyId']
        skill_domen = serializer.validated_data['skillDomen']

        team = get_object_or_404(EmployeeTeam, team__slug=team_slug)

        employees = self.get_employees(team, employee_id)

        employee_competencies = EmployeeCompetency.objects.filter(
            employee__in=employees,
            competency__id=competency_id,
            competency__competency_type=skill_domen,
        )

        serializer = EmployeeCompetencySerializer(
            employee_competencies, many=True
        )
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def get_employees(self, team, employee_id):
        return (
            team.employee.filter(id=employee_id)
            if employee_id
            else team.employee.all()
        )

    def method_not_allowed_response(self):
        return Response(
            {"error": "Method not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def error_response(self, errors):
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class TeamIndividualSkillsViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet для получения средних значений навыков сотрудника/команды.
    """

    serializer_class = SkillDomenRequestSerializer

    def create(self, request, team_slug: str, employee_id: Optional[int] = None) -> Response:
        """
        Создает запрос на получение средних значений навыков для сотрудников в команде.
        """
        if request.method != 'POST':
            return self.method_not_allowed_response()

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return self.error_response(serializer.errors)

        skill_domen = serializer.validated_data['skillDomen']
        team = get_object_or_404(EmployeeTeam, team__slug=team_slug)

        employee_id = request.data.get('employeeIds', employee_id)
        skills = self.get_skills(team, employee_id, skill_domen)

        skill_data = self.prepare_skill_data(skills, skill_domen)

        return Response({"data": skill_data}, status=status.HTTP_200_OK)

    def get_skills(self, team, employee_id, skill_domen):
        """
        Получаем навыки команды или сотрудников в команде.
        """
        if employee_id:
            return EmployeeSkill.objects.filter(
                employee__id__in=employee_id,
                employee__teams=team,
                skill__skill_type=skill_domen,
            )
        return EmployeeSkill.objects.filter(
            employee__teams=team,
            skill__skill_type=skill_domen,
        )

    def prepare_skill_data(self, skills, skill_domen):
        """
        Подготавливаем данные о навыках для ответа через сериализатор.
        """
        data = []
        for skill in skills:
            planned_avg = EmployeeSkill.objects.filter(
                skill__id=skill.skill.id
            ).aggregate(Avg('planned_result'))['planned_result__avg'] or 0

            actual_avg = EmployeeSkill.objects.filter(
                skill__id=skill.skill.id
            ).aggregate(Avg('actual_result'))['actual_result__avg'] or 0

            temp = {
                "skillDomen": skill_domen.capitalize(),
                "skillId": skill.skill.id,
                "skillName": skill.skill.skill_name,
                "plannedResult": round(planned_avg, 2),
                "actualResult": round(actual_avg, 2),
            }

            if not any(d['skillId'] == temp['skillId'] for d in data):
                data.append(temp)

        serializer = SkillSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)

        return serializer.data

    def method_not_allowed_response(self):
        return Response(
            {"error": "Method not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def error_response(self, errors):
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class SkillLevelViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """ViewSet для получения уровня навыков сотрудников."""

    serializer_class = SkillLevelRequestSerializer

    def create(self, request, team_slug, employee_id=None):
        """
        Создает запрос на получение уровня навыков сотрудников в команде.
        """
        if request.method != 'POST':
            return self.method_not_allowed_response()

        request_serializer = self.get_serializer(data=request.data)
        if not request_serializer.is_valid():
            return self.error_response(request_serializer.errors)

        skill_id = request_serializer.validated_data['skillId']
        team = get_object_or_404(EmployeeTeam, team__slug=team_slug)

        employees = self.get_employees(team, employee_id)

        employee_skills = EmployeeSkill.objects.filter(
            employee__in=employees,
            skill__id=skill_id,
        )

        if not employee_skills.exists():
            return Response({"data": []}, status=status.HTTP_200_OK)

        data = self.prepare_skill_data(employee_skills)
        return Response({"data": data}, status=status.HTTP_200_OK)

    def get_employees(self, team, employee_id):
        """Получаем сотрудников команды, фильтруя по employee_id, если передан."""
        return (
            team.employee.filter(id=employee_id)
            if employee_id
            else team.employee.all()
        )

    def prepare_skill_data(self, employee_skills):
        """Подготавливаем данные для ответа."""
        data = []
        for emp_skill in employee_skills:
            # Используем SkillColorSerializer для получения цвета
            color_serializer = SkillColorSerializer(data={'level': int(emp_skill.skill_level)})
            color_serializer.is_valid(raise_exception=True)
            color = color_serializer.get_color()

            data.append(
                {
                    "employeeId": emp_skill.employee.id,
                    "skillDomen": emp_skill.skill.skill_type.capitalize(),
                    "assessment": str(emp_skill.skill_level),
                    "color": color,
                }
            )

        serializer = SkillLevelSerializer(data, many=True)
        serializer.is_valid(raise_exception=True)
        return serializer.data

    def method_not_allowed_response(self):
        """Метод для обработки неподдерживаемых методов."""
        return Response(
            {"error": "Method not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def error_response(self, errors):
        """Метод для обработки ошибок валидации."""
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
