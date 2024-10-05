from django.contrib import admin
from core.models import (
    Employee, EmployeeKeyPeople, EmployeeBusFactor,
    EmployeeTrainingApplication, EmployeeGrade,
    EmployeeSkill, EmployeeCompetency, EmployeePosition
)


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
    extra = 1  # количество пустых форм для добавления новых записей


class EmployeeCompetencyInline(admin.TabularInline):
    model = EmployeeCompetency
    extra = 1


class EmployeeGradeInline(admin.TabularInline):
    model = EmployeeGrade
    extra = 1


class EmployeePositionInline(admin.TabularInline):
    model = EmployeePosition
    extra = 1


@admin.register(Employee)
class UserAdmin(admin.ModelAdmin):
    inlines = [
        EmployeeKeyPeopleInline,
        EmployeeBusFactorInline,
        EmployeeTrainingApplicationInline,
        EmployeeSkillInline,  # Инлайн для скиллов
        EmployeeCompetencyInline,  # Инлайн для компетенций
        EmployeeGradeInline,
        EmployeePositionInline
    ]

    list_display = (
        'pk', 'email', 'username', 'first_name', 'last_name'
    )
    search_fields = (
        'username', 'email', 'first_name', 'last_name'
    )
    list_filter = (
        'username', 'email'
    )