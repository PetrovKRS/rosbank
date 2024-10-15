from django.contrib import admin

from core.models import (
    Employee,
    DevelopmentPlan,
    EmployeeDevelopmentPlan,
    Engagement,
    EmployeeEngagement,
    KeyPeople,
    EmployeeKeyPeople,
    TrainingApplication,
    EmployeeTrainingApplication,
    BusFactor,
    EmployeeBusFactor,
    Grade,
    EmployeeGrade,
    KeySkill,
    EmployeeKeySkill,
    Team,
    EmployeeTeam,
    Position,
    EmployeePosition,
    PositionCompetency,
    TeamPosition,
    Competency,
    EmployeeCompetency,
    Skill,
    EmployeeSkill,
    SkillForCompetency,
    ExpectedSkill,
    EmployeeExpectedSkill,
    CompetencyForExpectedSkill,
)


@admin.register(DevelopmentPlan)
class DevelopmentPlanAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'plan_name',
        'employee_count',
    )
    readonly_fields = ('employee_count',)


@admin.register(EmployeeDevelopmentPlan)
class EmployeeDevelopmentPlanAdmin(admin.ModelAdmin):
    list_display = (
        'employee',
        'development_plan',
        'performance_score',
        'add_date',
    )
    fields = (
        'employee',
        'development_plan',
        'performance_score',
    )


@admin.register(Engagement)
class EngagementAdmin(admin.ModelAdmin):
    readonly_fields = ('employee_count',)


@admin.register(EmployeeEngagement)
class EmployeeEngagementAdmin(admin.ModelAdmin):
    list_display = (
        'employee',
        'engagement',
        'performance_score',
        'add_date',
    )


@admin.register(KeyPeople)
class KeyPeopleAdmin(admin.ModelAdmin):
    readonly_fields = ('employee_count',)


@admin.register(EmployeeKeyPeople)
class EmployeeKeyPeopleAdmin(admin.ModelAdmin):
    list_display = ('add_date',)


@admin.register(TrainingApplication)
class TrainingApplicationAdmin(admin.ModelAdmin):
    readonly_fields = ('employee_count',)


@admin.register(EmployeeTrainingApplication)
class EmployeeTrainingApplicationAdmin(admin.ModelAdmin):
    pass


@admin.register(BusFactor)
class BusFactorAdmin(admin.ModelAdmin):
    readonly_fields = ('employee_count',)


@admin.register(EmployeeBusFactor)
class EmployeeBusFactorAdmin(admin.ModelAdmin):
    list_display = ('add_date',)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    pass


@admin.register(EmployeeGrade)
class EmployeeGradeAdmin(admin.ModelAdmin):
    pass


@admin.register(KeySkill)
class KeySkillAdmin(admin.ModelAdmin):
    readonly_fields = ('employee_count',)


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
        return ", ".join(
            [employee.__str__() for employee in obj.employee.all()]
        )

    get_employees.short_description = 'Сотрудники'


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    readonly_fields = ('grade_count',)


@admin.register(EmployeePosition)
class EmployeePositionAdmin(admin.ModelAdmin):
    pass


@admin.register(Competency)
class CompetencyAdmin(admin.ModelAdmin):
    readonly_fields = ('employee_count',)


@admin.register(EmployeeCompetency)
class EmployeeCompetencyAdmin(admin.ModelAdmin):
    fields = (
        'employee',
        'competency',
        'competency_level',
        'planned_result',
        'actual_result',
    )

    list_display = (
        'employee',
        'competency',
        'competency_level',
        'planned_result',
        'actual_result',
    )

    list_filter = ('competency',)

    search_fields = (
        'employee__name',
        'competency__competency_name',
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    readonly_fields = ('employee_count',)


@admin.register(EmployeeSkill)
class EmployeeSkillAdmin(admin.ModelAdmin):
    pass


@admin.register(EmployeeExpectedSkill)
class EmployeeExpectedSkillAdmin(admin.ModelAdmin):
    pass
