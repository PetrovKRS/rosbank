from django.contrib import admin
from .models import (
    DevelopmentPlan, EmployeeDevelopmentPlan, Engagement, EmployeeEngagement,
    KeyPeople, EmployeeKeyPeople, TrainingApplication, EmployeeTrainingApplication,
    BusFactor, EmployeeBusFactor, Grade, EmployeeGrade, KeySkill, EmployeeKeySkill,
    Team, EmployeeTeam, Position, EmployeePosition, Competency, PositionCompetency,
    TeamPosition, EmployeeCompetency, Skill, EmployeeSkill, SkillForCompetency,
    ExpectedSkill, EmployeeExpectedSkill, CompetencyForExpectedSkill
)

@admin.register(DevelopmentPlan)
class DevelopmentPlanAdmin(admin.ModelAdmin):
    list_display = ('plan_name', 'employee_count')
    search_fields = ('plan_name',)

@admin.register(EmployeeDevelopmentPlan)
class EmployeeDevelopmentPlanAdmin(admin.ModelAdmin):
    list_display = ('employee', 'development_plan', 'development_progress')
    search_fields = ('employee__name', 'development_plan__plan_name')

@admin.register(Engagement)
class EngagementAdmin(admin.ModelAdmin):
    list_display = ('engagement_name', 'employee_count')
    search_fields = ('engagement_name',)

@admin.register(EmployeeEngagement)
class EmployeeEngagementAdmin(admin.ModelAdmin):
    list_display = ('employee', 'engagement', 'engagement_level')
    search_fields = ('employee__name', 'engagement__engagement_name')

@admin.register(KeyPeople)
class KeyPeopleAdmin(admin.ModelAdmin):
    list_display = ('key_people_name', 'employee_count')
    search_fields = ('key_people_name',)

@admin.register(EmployeeKeyPeople)
class EmployeeKeyPeopleAdmin(admin.ModelAdmin):
    list_display = ('employee', 'key_people')
    search_fields = ('employee__name', 'key_people__key_people_name')

@admin.register(TrainingApplication)
class TrainingApplicationAdmin(admin.ModelAdmin):
    list_display = ('training_name', 'employee_count')
    search_fields = ('training_name',)

@admin.register(EmployeeTrainingApplication)
class EmployeeTrainingApplicationAdmin(admin.ModelAdmin):
    list_display = ('employee', 'training_application')
    search_fields = ('employee__name', 'training_application__training_name')

@admin.register(BusFactor)
class BusFactorAdmin(admin.ModelAdmin):
    list_display = ('bus_factor_name', 'employee_count')
    search_fields = ('bus_factor_name',)

@admin.register(EmployeeBusFactor)
class EmployeeBusFactorAdmin(admin.ModelAdmin):
    list_display = ('employee', 'bus_factor')
    search_fields = ('employee__name', 'bus_factor__bus_factor_name')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('grade_name',)
    search_fields = ('grade_name',)

@admin.register(EmployeeGrade)
class EmployeeGradeAdmin(admin.ModelAdmin):
    list_display = ('employee', 'grade')
    search_fields = ('employee__name', 'grade__grade_name')

@admin.register(KeySkill)
class KeySkillAdmin(admin.ModelAdmin):
    list_display = ('skill_name', 'employee_count')
    search_fields = ('skill_name',)

@admin.register(EmployeeKeySkill)
class EmployeeKeySkillAdmin(admin.ModelAdmin):
    list_display = ('employee', 'key_skill', 'skill_level')
    search_fields = ('employee__name', 'key_skill__skill_name')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name',)
    search_fields = ('team_name',)

@admin.register(EmployeeTeam)
class EmployeeTeamAdmin(admin.ModelAdmin):
    list_display = ('employee', 'team')
    search_fields = ('employee__name', 'team__team_name')

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('position_name', 'grade_count')
    search_fields = ('position_name',)

@admin.register(EmployeePosition)
class EmployeePositionAdmin(admin.ModelAdmin):
    list_display = ('employee', 'position')
    search_fields = ('employee__name', 'position__position_name')

@admin.register(Competency)
class CompetencyAdmin(admin.ModelAdmin):
    list_display = ('competency_name', 'employee_count')
    search_fields = ('competency_name',)

@admin.register(PositionCompetency)
class PositionCompetencyAdmin(admin.ModelAdmin):
    list_display = ('position', 'competency')
    search_fields = ('position__position_name', 'competency__competency_name')

@admin.register(TeamPosition)
class TeamPositionAdmin(admin.ModelAdmin):
    list_display = ('team', 'position')
    search_fields = ('team__team_name', 'position__position_name')

@admin.register(EmployeeCompetency)
class EmployeeCompetencyAdmin(admin.ModelAdmin):
    list_display = ('employee', 'competency', 'competency_level')
    search_fields = ('employee__name', 'competency__competency_name')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('skill_name', 'employee_count')
    search_fields = ('skill_name',)

@admin.register(EmployeeSkill)
class EmployeeSkillAdmin(admin.ModelAdmin):
    list_display = ('employee', 'skill', 'skill_level')
    search_fields = ('employee__name', 'skill__skill_name')

@admin.register(SkillForCompetency)
class SkillForCompetencyAdmin(admin.ModelAdmin):
    list_display = ('skill', 'competency')
    search_fields = ('skill__skill_name', 'competency__competency_name')

@admin.register(ExpectedSkill)
class ExpectedSkillAdmin(admin.ModelAdmin):
    list_display = ('expected_skill_name', 'employee_count')
    search_fields = ('expected_skill_name',)

@admin.register(EmployeeExpectedSkill)
class EmployeeExpectedSkillAdmin(admin.ModelAdmin):
    list_display = ('employee', 'expected_skill')
    search_fields = ('employee__name', 'expected_skill__expected_skill_name')

@admin.register(CompetencyForExpectedSkill)
class CompetencyForExpectedSkillAdmin(admin.ModelAdmin):
    list_display = ('expected_skill', 'competency')
    search_fields = ('expected_skill__expected_skill_name', 'competency__competency_name')


