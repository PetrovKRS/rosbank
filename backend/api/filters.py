from django_filters import rest_framework as filters
from core.models import Employee


class EmployeeFilter(filters.FilterSet):
    position = filters.CharFilter(
        field_name='positions__position__position_name',
        lookup_expr='exact',
        label='Должность сотрудника',
        help_text='Должность сотрудника',
    )
    grade = filters.CharFilter(
        field_name='grades__grade__grade_name',
        lookup_expr='exact',
        label='Класс сотрудника',
        help_text='Класс сотрудника',
    )
    skill = filters.CharFilter(
        field_name='skills__skill__skill_name',
        lookup_expr='exact',
        label='Навык сотрудника',
    )
    competency = filters.CharFilter(
        field_name='employee_competencies__competency__competency_name',
        lookup_expr='exact',
        label='Компетенция сотрудника',
        help_text='Компетенция сотрудника',
    )
    worker = filters.CharFilter(
        method='filter_by_full_name',
        label='Полное имя сотрудника',
    )

    class Meta:
        model = Employee
        fields = ('position', 'grade', 'skill', 'competency', 'worker')

    def filter_by_name(self, queryset, name, value):
        parts = value.split()
        first_name, last_name = parts
        return queryset.filter(
            first_name__exact=first_name, last_name__exact=last_name
        )
