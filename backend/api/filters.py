from django_filters import rest_framework as filters
from django.db.models import Q

from core.models import Employee


class EmployeeFilter(filters.FilterSet):
    """Фильтр сотрудников."""

    position = filters.CharFilter(
        field_name='positions__position__position_name', lookup_expr='exact'
    )
    grade = filters.CharFilter(
        field_name='grades__grade__grade_name', lookup_expr='exact'
    )
    skill = filters.CharFilter(
        field_name='skills__skill__skill_name', lookup_expr='exact'
    )
    competency = filters.CharFilter(
        field_name='competencies__competency__competency_name'
    )
    name = filters.CharFilter(
        method='filter_by_name',
    )

    class Meta:
        model = Employee
        fields = ('position', 'grade', 'skill', 'competency', 'name')

    def filter_by_name(self, queryset, name, value):

        parts = value.split()
        query = Q()

        for part in parts:
            query |= Q(first_name__icontains=part) | Q(
                last_name__icontains=part
            )

        return queryset.filter(query)
