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
        method='filter_by_full_name',
        label='Полное имя сотрудника',
    )

    class Meta:
        model = Employee
        fields = ('position', 'grade', 'skill', 'competency', 'worker',)

    def filter_by_full_name(self, queryset, name, value):
        # Разделение значения на имя и фамилию
        name_parts = value.strip().split(' ')
        if len(name_parts) == 2:
            first_name, last_name = name_parts
            return queryset.filter(
                first_name__icontains=first_name,
                last_name__icontains=last_name
            )
        return queryset.none()  # Возвращаем пустой набор, если значение не подходит под формат
