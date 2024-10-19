from django_filters import rest_framework as filters
from core.models import Employee
from django.db.models import Q


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
        field_name='employee__first_name ' + 'employee__last_name',
        lookup_expr='icontains',
        # method='filter_by_name',
        label='ФИО сотрудника',
        help_text='ФИО сотрудника'
    )

    class Meta:
        model = Employee
        fields = ('position', 'grade', 'skill', 'competency', 'worker',)

    def filter_by_name(self, queryset, name, value):
        parts = value.split()
        query = Q()


        for part in parts:
            query |= Q(first_name__icontains=part) | Q(last_name__icontains=part)

        return queryset.filter(query)