from django.contrib import admin

from core.models import (
    DevelopmentPlan,
    Engagement,
    KeyPeople,
    TrainingApplication,
    BusFactor,
    Grade,
    KeySkill,
    Team,
    EmployeeTeam,
    Position,
    Competency,
    Skill,
    AssesmentSkill,
    EmployeeAssesmentSkill,
)

#
# @admin.register(Employee)
# class EmployeeAdmin(admin.ModelAdmin):
#     pass
#     list_display = (
#         'pk', 'first_name', 'last_name', 'email', 'status',
#         'registration_date', 'last_login_date',
#     )


@admin.register(AssesmentSkill)
class AssesmentSkillAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'assesment_name',
    )
   


@admin.register(EmployeeAssesmentSkill)
class EmployeeAssesmentSkillAdmin(admin.ModelAdmin):
    list_display = (
        'assesment',
    )


@admin.register(DevelopmentPlan)
class DevelopmentPlanAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'plan_name',
        'employee_count',
    )
    readonly_fields = ('employee_count',)


# @admin.register(EmployeeDevelopmentPlan)
# class EmployeeDevelopmentPlanAdmin(admin.ModelAdmin):
#     list_display = (
#         'employee', 'development_plan', 'performance_score',
#         'add_date',
#     )
#     fields = (
#         'employee', 'development_plan', 'performance_score',
#     )


@admin.register(Engagement)
class EngagementAdmin(admin.ModelAdmin):
    readonly_fields = ('employee_count',)


# @admin.register(EmployeeEngagement)
# class EmployeeEngagementAdmin(admin.ModelAdmin):
#     list_display = (
#         'employee', 'engagement', 'performance_score', 'add_date',
#     )


@admin.register(KeyPeople)
class KeyPeopleAdmin(admin.ModelAdmin):
    readonly_fields = ('employee_count',)


# @admin.register(EmployeeKeyPeople)
# class EmployeeKeyPeopleAdmin(admin.ModelAdmin):
#     list_display = (
#         'add_date',
#     )


@admin.register(TrainingApplication)
class TrainingApplicationAdmin(admin.ModelAdmin):
    readonly_fields = ('employee_count',)


@admin.register(BusFactor)
class BusFactorAdmin(admin.ModelAdmin):
    readonly_fields = ('employee_count',)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    pass


@admin.register(KeySkill)
class KeySkillAdmin(admin.ModelAdmin):
    readonly_fields = ('employee_count',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(EmployeeTeam)
class EmployeeTeamAdmin(admin.ModelAdmin):
    list_display = ('manager', 'team', 'get_employees')

    def get_employees(self, obj):
        return ", ".join(
            [employee.__str__() for employee in obj.employee.all()]
        )

    get_employees.short_description = 'Сотрудники'


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    readonly_fields = ('grade_count',)


@admin.register(Competency)
class CompetencyAdmin(admin.ModelAdmin):
    readonly_fields = ('employee_count',)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    readonly_fields = ('employee_count',)
