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
        # Разделяем строку поиска на имя и фамилию
        search_terms = value.split()

        if len(search_terms) == 2:
            # Ищем по двум полям, если введено имя и фамилия
            first_name, last_name = search_terms
            return queryset.filter(
                Q(first_name__icontains=first_name) & Q(last_name__icontains=last_name)
            )
        elif len(search_terms) == 1:
            # Ищем по одному из полей, если введено только одно слово
            return queryset.filter(
                Q(first_name__icontains=value) | Q(last_name__icontains=value)
            )
        return queryset
