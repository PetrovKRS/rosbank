from rest_framework import serializers
from users.models import Employee
from core.models import (
    DevelopmentPlan, EmployeeDevelopmentPlan, EmployeeEngagement,
    KeyPeople, EmployeeKeyPeople, TrainingApplication, EmployeeTrainingApplication,
    BusFactor, EmployeeBusFactor, Grade, EmployeeGrade, KeySkill, EmployeeKeySkill,
    Team, EmployeeTeam, Position, EmployeePosition, Competency, PositionCompetency,
    TeamPosition, EmployeeCompetency, Skill, EmployeeSkill, SkillForCompetency,
    ExpectedSkill, EmployeeExpectedSkill, CompetencyForExpectedSkill
)
from django.urls import reverse
from rest_framework.validators import UniqueTogetherValidator


class WorkersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'employee_id', 'first_name', 'patronymic', 'position')


# Сериализатор для навыков сотрудника
class SkillSerializer(serializers.ModelSerializer):
    skill = serializers.CharField(source='skill.skill_name')

    class Meta:
        model = EmployeeSkill
        fields = ['skill', 'skill_level']


# Сериализатор для компетенций сотрудника
class CompetencySerializer(serializers.ModelSerializer):
    competency = serializers.CharField(source='competency.competency_name')

    class Meta:
        model = EmployeeCompetency
        fields = ['competency', 'competency_level']


# Основной сериализатор для сотрудников
class EmployeeSerializer(serializers.ModelSerializer):
    worker = serializers.SerializerMethodField()
    skills = SkillSerializer(many=True)
    competencies = CompetencySerializer(source='employeecompetency_set', many=True)
    position = serializers.CharField(source='positions.first.position.position_name', allow_null=True)
    grade = serializers.CharField(source='grades.grade.grade_name', )

    key_people = serializers.SerializerMethodField()
    bus_factor = serializers.SerializerMethodField()
    education = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'position', 'worker', 'grade', 'key_people', 'bus_factor', 'education', 'skills',
                  'competencies']

    def get_worker(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    # Проверка наличия записи в EmployeeKeyPeople
    def get_key_people(self, obj):
        return EmployeeKeyPeople.objects.filter(employee=obj).exists()

    # Проверка наличия записи в EmployeeBusFactor
    def get_bus_factor(self, obj):
        return EmployeeBusFactor.objects.filter(employee=obj).exists()

    # Проверка наличия записи в EmployeeTrainingApplication (образование)
    def get_education(self, obj):
        return EmployeeTrainingApplication.objects.filter(employee=obj).exists()

    # def get_grade(self, obj):
    #     try:
    #         return obj.employeegrade.grade.grade_name
    #     except EmployeeGrade.DoesNotExist:
    #         return None

    # def get_position(self, obj):
    #     try:
    #         return obj.employeeposition_set.first().position  # Получаем первую связанную позицию
    #     except (AttributeError, EmployeePosition.DoesNotExist):
    #         return None
    