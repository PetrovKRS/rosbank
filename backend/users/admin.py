from django.contrib import admin
from core.models import (
    Employee,
    EmployeeKeyPeople,
    EmployeeBusFactor,
    EmployeeTrainingApplication,
    EmployeeGrade,
    EmployeeSkill,
    EmployeeCompetency,
    EmployeePosition,
    EmployeeDevelopmentPlan,
    EmployeeEngagement,
    AssesmentSkill
)
from users.models import ManagerTeam

from core.models import EmployeeAssesmentSkill


class EmployeeKeyPeopleInline(admin.TabularInline):
    model = EmployeeKeyPeople
    extra = 1


class EmployeeBusFactorInline(admin.TabularInline):
    model = EmployeeBusFactor
    extra = 1


class EmployeeTrainingApplicationInline(admin.TabularInline):
    model = EmployeeTrainingApplication
    extra = 1


class EmployeeSkillInline(admin.TabularInline):
    model = EmployeeSkill
    extra = 1


class EmployeeCompetencyInline(admin.TabularInline):
    model = EmployeeCompetency
    extra = 1


class EmployeeGradeInline(admin.TabularInline):
    model = EmployeeGrade
    extra = 1


class EmployeePositionInline(admin.TabularInline):
    model = EmployeePosition
    extra = 1


class EmployeeDevelopmentPlanInline(admin.TabularInline):
    model = EmployeeDevelopmentPlan
    extra = 1


class EmployeeEngagementInline(admin.TabularInline):
    model = EmployeeEngagement
    extra = 1


class EmployeeAssesmentSkillInline(admin.TabularInline):
    model = EmployeeAssesmentSkill
    extra = 1


@admin.register(Employee)
class UserAdmin(admin.ModelAdmin):
    inlines = [
        EmployeeKeyPeopleInline,
        EmployeeBusFactorInline,
        EmployeeTrainingApplicationInline,
        EmployeeSkillInline,
        EmployeeCompetencyInline,
        EmployeeGradeInline,
        EmployeePositionInline,
        EmployeeDevelopmentPlanInline,
        EmployeeEngagementInline,
        EmployeeAssesmentSkillInline
    ]

    list_display = ('pk', 'employee_id', 'email', 'first_name', 'last_name')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('email', 'first_name', 'last_name')


@admin.register(ManagerTeam)
class ManagerTeamAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_superuser',
    )
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = (
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_superuser',
    )
