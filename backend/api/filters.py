from django_filters import rest_framework as filters
from users.models import Employee


class EmployeeFilter(filters.FilterSet):
    position = filters.CharFilter(
        field_name='positions__position__position_name',
        lookup_expr='exact'
    )
    grade = filters.CharFilter(
        field_name='grades__grade__grade_name',
        lookup_expr='exact'
    )
    skill = filters.CharFilter(
        field_name='skills__skill__skill_name',
        lookup_expr='exact'
    )
    competency = filters.CharFilter(
        field_name='competencies__competency__competency_name'
    )
    criterion = filters.CharFilter(
        field_name='criterion',
        lookup_expr='icontains'
    )

    class Meta:
        model = Employee
        fields = (
            'position', 'grade', 'skill', 'competency', 'criterion'
        )


class EmployeeKeySkillFilter(filters.FilterSet):
    criterion = filters.CharFilter(
        field_name="key_skills__key_skill__skill_name",
        lookup_expr='exact'
    )
    month = filters.CharFilter(
        field_name="development_plans__month",
        lookup_expr='exact'
    )
    year = filters.NumberFilter(
        field_name="development_plans__year",
        lookup_expr='exact'
    )

    class Meta:
        model = Employee
        fields = (
            'criterion',
        )