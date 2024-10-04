from django.contrib import admin

from .models import (
    Employee, DevelopmentPlan, EmployeeDevelopmentPlan,
    Engagement, EmployeeEngagement, KeyPeople,
    EmployeeKeyPeople, TrainingApplication,
    EmployeeTrainingApplication, BusFactor, EmployeeBusFactor,
    Grade, EmployeeGrade, KeySkill, EmployeeKeySkill,
    Team, EmployeeTeam, Position, EmployeePosition, PositionCompetency,
    TeamPosition, EmployeePosition, Competency, EmployeeCompetency,
    Skill, EmployeeSkill, SkillForCompetency, ExpectedSkill,
    EmployeeExpectedSkill, CompetencyForExpectedSkill,
)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'last_name', 'email', 'status',
        'registration_date', 'last_login_date',
    )
    # search_fields = (
    #     'username', 'email', 'first_name', 'last_name'
    # )
    # list_filter = (
    #     'username', 'email'
    # )
    # empty_value_display = '- пусто -'


@admin.register(DevelopmentPlan)
class DevelopmentPlanAdmin(admin.ModelAdmin):
    pass


@admin.register(EmployeeDevelopmentPlan)
class EmployeeDevelopmentPlanAdmin(admin.ModelAdmin):
    pass


@admin.register(Engagement)
class EngagementAdmin(admin.ModelAdmin):
    pass


@admin.register(EmployeeEngagement)
class EmployeeEngagementAdmin(admin.ModelAdmin):
    pass


@admin.register(KeyPeople)
class KeyPeopleAdmin(admin.ModelAdmin):
    pass


@admin.register(EmployeeKeyPeople)
class EmployeeKeyPeopleAdmin(admin.ModelAdmin):
    pass


@admin.register(TrainingApplication)
class TrainingApplicationAdmin(admin.ModelAdmin):
    pass


@admin.register(EmployeeTrainingApplication)
class EmployeeTrainingApplicationAdmin(admin.ModelAdmin):
    pass


@admin.register(BusFactor)
class BusFactorAdmin(admin.ModelAdmin):
    pass


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
    pass


@admin.register(EmployeeKeySkill)
class EmployeeKeySkillAdmin(admin.ModelAdmin):
    pass


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(EmployeeTeam)
class EmployeeTeamAdmin(admin.ModelAdmin):
    pass


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    pass


@admin.register(EmployeePosition)
class EmployeePositionAdmin(admin.ModelAdmin):
    pass


@admin.register(PositionCompetency)
class PositionCompetencyAdmin(admin.ModelAdmin):
    pass


@admin.register(TeamPosition)
class TeamPositionAdmin(admin.ModelAdmin):
    pass


@admin.register(EmployeePosition)
class EmployeePositionAdmin(admin.ModelAdmin):
    pass


@admin.register(Competency)
class CompetencyAdmin(admin.ModelAdmin):
    pass


@admin.register(EmployeeCompetency)
class EmployeeCompetencyAdmin(admin.ModelAdmin):
    pass


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    pass


@admin.register(EmployeeSkill)
class EmployeeSkillAdmin(admin.ModelAdmin):
    pass


@admin.register(SkillForCompetency)
class SkillForCompetencyAdmin(admin.ModelAdmin):
    pass


@admin.register(ExpectedSkill)
class ExpectedSkillAdmin(admin.ModelAdmin):
    pass


@admin.register(EmployeeExpectedSkill)
class EmployeeExpectedSkillAdmin(admin.ModelAdmin):
    pass


@admin.register(CompetencyForExpectedSkill)
class CompetencyForExpectedSkillAdmin(admin.ModelAdmin):
    pass
