from django.contrib import admin

from .models import (
    Employee, DevelopmentPlan, EmployeeDevelopmentPlan,
    Engagement, EmployeeEngagement, KeyPeople,
    EmployeeKeyPeople, TrainingApplication,
    EmployeeTrainingApplication, BusFactor, EmployeeBusFactor,
    Grade, EmployeeGrade, KeySkill, EmployeeKeySkill,
    Team, EmployeeTeam, Position, EmployeePosition, PositionCompetency,
    TeamPosition, Competency, EmployeeCompetency,
    Skill, EmployeeSkill, SkillForCompetency, ExpectedSkill,
    EmployeeExpectedSkill, CompetencyForExpectedSkill,
)


# @admin.register(Employee)
# class EmployeeAdmin(admin.ModelAdmin):
#     pass
#     list_display = (
#         'pk', 'first_name', 'last_name', 'email', 'status',
#         'registration_date', 'last_login_date',
#     )


@admin.register(DevelopmentPlan)
class DevelopmentPlanAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'plan_name', 'employee_count',
    )
    readonly_fields = (
        'employee_count',
    )


@admin.register(EmployeeDevelopmentPlan)
class EmployeeDevelopmentPlanAdmin(admin.ModelAdmin):
    pass


@admin.register(Engagement)
class EngagementAdmin(admin.ModelAdmin):
    readonly_fields = (
        'employee_count',
    )


@admin.register(EmployeeEngagement)
class EmployeeEngagementAdmin(admin.ModelAdmin):
    pass


@admin.register(KeyPeople)
class KeyPeopleAdmin(admin.ModelAdmin):
    readonly_fields = (
        'employee_count',
    )


@admin.register(EmployeeKeyPeople)
class EmployeeKeyPeopleAdmin(admin.ModelAdmin):
    pass


@admin.register(TrainingApplication)
class TrainingApplicationAdmin(admin.ModelAdmin):
    readonly_fields = (
        'employee_count',
    )


@admin.register(EmployeeTrainingApplication)
class EmployeeTrainingApplicationAdmin(admin.ModelAdmin):
    pass


@admin.register(BusFactor)
class BusFactorAdmin(admin.ModelAdmin):
    readonly_fields = (
        'employee_count',
    )


@admin.register(EmployeeBusFactor)
class EmployeeBusFactorAdmin(admin.ModelAdmin):
    pass


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    pass


@admin.register(EmployeeGrade)
class EmployeeGradeAdmin(admin.ModelAdmin):
    pass


@admin.register(KeySkill)
class KeySkillAdmin(admin.ModelAdmin):
    readonly_fields = (
        'employee_count',
    )


@admin.register(EmployeeKeySkill)
class EmployeeKeySkillAdmin(admin.ModelAdmin):
    pass


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(EmployeeTeam)
class EmployeeTeamAdmin(admin.ModelAdmin):
    list_display = ('manager', 'team', 'get_employees')

    def get_employees(self, obj):
        return ", ".join([employee.__str__() for employee in obj.employee.all()])
    get_employees.short_description = 'Сотрудники'


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    readonly_fields = (
        'grade_count',
    )


@admin.register(EmployeePosition)
class EmployeePositionAdmin(admin.ModelAdmin):
    pass


# @admin.register(PositionCompetency)
# class PositionCompetencyAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(TeamPosition)
# class TeamPositionAdmin(admin.ModelAdmin):
#     pass


@admin.register(Competency)
class CompetencyAdmin(admin.ModelAdmin):
    readonly_fields = (
        'employee_count',
    )


@admin.register(EmployeeCompetency)
class EmployeeCompetencyAdmin(admin.ModelAdmin):
    pass


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    readonly_fields = (
        'employee_count',
    )


@admin.register(EmployeeSkill)
class EmployeeSkillAdmin(admin.ModelAdmin):
    pass


# @admin.register(SkillForCompetency)
# class SkillForCompetencyAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(ExpectedSkill)
# class ExpectedSkillAdmin(admin.ModelAdmin):
#     pass


@admin.register(EmployeeExpectedSkill)
class EmployeeExpectedSkillAdmin(admin.ModelAdmin):
    pass


# @admin.register(CompetencyForExpectedSkill)
# class CompetencyForExpectedSkillAdmin(admin.ModelAdmin):
#     pass
