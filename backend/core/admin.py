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
    SkillForCompetency,
)


@admin.register(AssesmentSkill)
class AssesmentSkillAdmin(admin.ModelAdmin):
    pass


@admin.register(EmployeeAssesmentSkill)
class EmployeeAssesmentSkillAdmin(admin.ModelAdmin):
    pass


@admin.register(DevelopmentPlan)
class DevelopmentPlanAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'plan_name',
        'employee_count',
    )
    readonly_fields = ('employee_count',)


@admin.register(Engagement)
class EngagementAdmin(admin.ModelAdmin):
    readonly_fields = ('employee_count',)


@admin.register(KeyPeople)
class KeyPeopleAdmin(admin.ModelAdmin):
    readonly_fields = ('employee_count',)


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


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    readonly_fields = ('employee_count',)


class SkillForCompetency(admin.TabularInline):
    model = SkillForCompetency
    extra = 1


@admin.register(Competency)
class CompetencyAdmin(admin.ModelAdmin):
    inlines = (SkillForCompetency,)
    list_display = (
        'pk',
        'competency_name',
    )
    readonly_fields = ('employee_count',)
