# Стандартные библиотеки
from django.urls import reverse
from django.db.models import Avg

# Сторонние библиотеки
from rest_framework import serializers

# Модули текущего проекта
from core.models import (
    EmployeeKeyPeople,
    EmployeeTrainingApplication,
    EmployeeBusFactor,
    EmployeeCompetency,
    Skill,
    EmployeeSkill,
    SkillTypeEnum,
    Employee,
    EmployeeKeyPeople,
    EmployeeTrainingApplication,
    EmployeeBusFactor,
    EmployeeCompetency,
    Skill,
    EmployeeSkill,
    SkillTypeEnum,
    Employee,
)


class WorkersSerializer(serializers.ModelSerializer):
    '''Сериализатор для сотрудников.'''

    class Meta:
        model = Employee
        fields = ('id', 'employee_id', 'first_name', 'patronymic', 'position')


class SkillSerializer(serializers.ModelSerializer):
    """Сериализатор для навыков сотрудника."""

    skill = serializers.CharField(source='skill.skill_name')

    class Meta:
        model = EmployeeSkill
        fields = ('skill', 'skill_level')


class CompetencySerializer(serializers.ModelSerializer):
    """Сериализатор для компетенций сотрудника."""

    competency = serializers.CharField(source='competency.competency_name')

    class Meta:
        model = EmployeeCompetency
        fields = ('competency', 'competency_level')


class TrainingApplicationSerializer(serializers.ModelSerializer):
    """Сериализатор для заявок на обучение."""

    training_name = serializers.CharField(
        source='training_application.training_name'
    )

    class Meta:
        model = EmployeeTrainingApplication
        fields = (
            'id',
            'training_name',
        )


class AssesmentOfPotentionSerializer(serializers.Serializer):
    """Сериализатор для оценки потенциала сотрудника."""

    assesmentLevel = serializers.SerializerMethodField()
    involvmentLevel = serializers.IntegerField(
        source='engagements.performance_score', default=0
    )

    def get_assesmentLevel(self, obj):
        average_assessment = obj.assesments_skills.aggregate(Avg('assesment'))[
            'assesment__avg'
        ]
        # Если есть средняя оценка, возвращаем её, иначе возвращаем 0
        return average_assessment if average_assessment is not None else 0


class EmployeeSerializer(serializers.ModelSerializer):
    """Основной сериализатор для сотрудников."""

    worker = serializers.SerializerMethodField()
    position = serializers.CharField(
        source='positions.position.position_name', allow_null=True
    )
    grade = serializers.CharField(
        source='grades.grade.grade_name',
    )
    assesmentOfPotention = AssesmentOfPotentionSerializer(source='*')

    key_people = serializers.SerializerMethodField()
    bus_factor = serializers.SerializerMethodField()
    education = TrainingApplicationSerializer(
        source='training_applications', many=True
    )
    skill = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            'id',
            'position',
            'worker',
            'grade',
            'key_people',
            'bus_factor',
            'education',
            'assesmentOfPotention',
            'skill',
        )

    def get_worker(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_skill(self, obj):
        """Рассчитывает средний уровень навыков сотрудника."""
        average_skill_level = obj.skills.aggregate(
            avg_level=Avg('skill_level')
        )['avg_level']
        return (
            int(average_skill_level) if average_skill_level is not None else 0
        )

    def get_key_people(self, obj):
        '''Проверяем наличие ключевых людей у сотрудника.'''
        return EmployeeKeyPeople.objects.filter(employee=obj).exists()

    def get_bus_factor(self, obj):
        '''Проверяем наличие bus-фактора у сотрудника.'''
        return EmployeeBusFactor.objects.filter(employee=obj).exists()

    def get_education(self, obj):
        '''Проверяем наличие обучения у сотрудника.'''
        return EmployeeTrainingApplication.objects.filter(
            employee=obj
        ).exists()


class MetricRequestSerializer(serializers.Serializer):
    '''Сериализатор для запроса метрик.'''

    employeeIds = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    startPeriod = serializers.DateField(required=True)
    endPeriod = serializers.DateField(required=True)


class PeriodSerializer(serializers.Serializer):
    '''Сериализатор для периода.'''

    month = serializers.CharField(required=True)
    year = serializers.CharField(required=True)


class TimePeriodRequestSerializer(serializers.Serializer):
    '''Сериализатор для запроса периода.'''

    startPeriod = PeriodSerializer(required=True)
    endPeriod = PeriodSerializer(required=True)


class IndividualDevelopmentPlanResponseSerializer(serializers.Serializer):
    '''Сериализатор для ответа на запрос индивидуального плана.'''

    dashboard = serializers.ListField(child=serializers.DictField())
    completionForToday = serializers.CharField()


class PeriodSerializer(serializers.Serializer):
    '''Сериализатор для периода.'''

    month = serializers.CharField(max_length=20)
    year = serializers.IntegerField()


class SkillDataSerializer(serializers.Serializer):
    '''Сериализатор для данных навыка.'''

    skillId = serializers.IntegerField()
    skillName = serializers.CharField(max_length=100)
    assesment = serializers.IntegerField()


class TeamSkillAssessmentResponseSerializer(serializers.Serializer):
    '''Сериализатор для ответа на запрос оценки навыков.'''

    period = PeriodSerializer()
    skillsData = serializers.ListField(child=SkillDataSerializer())


class SkillDomenRequestSerializer(serializers.Serializer):
    '''Сериализатор для запроса навыков.'''

    skillDomen = serializers.ChoiceField(
        choices=SkillTypeEnum.choices(), help_text="Тип навыка: hard или soft"
    )


class CompetencySerializer(serializers.Serializer):
    '''Сериализатор для компетенции.'''

    competencyId = serializers.IntegerField()
    skillDomen = serializers.CharField()
    competencyName = serializers.CharField()
    plannedResult = serializers.FloatField()
    actualResult = serializers.FloatField()


class CompetencyLevelRequestSerializer(serializers.Serializer):
    '''Сериализатор для запроса компетенции.'''

    competencyId = serializers.IntegerField()


class EmployeeCompetencySerializer(serializers.ModelSerializer):
    '''Сериализатор для компетенции сотрудника.'''

    employeeId = serializers.IntegerField(source='employee.id', read_only=True)
    skillDomen = serializers.SerializerMethodField()
    assessment = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()

    class Meta:
        model = EmployeeCompetency
        fields = ['employeeId', 'skillDomen', 'assessment', 'color']

    def get_skillDomen(self, obj):
        """
        Получаем тип компетенции и возвращаем его с первой заглавной буквой.
        """
        return obj.competency.competency_type

    def get_assessment(self, obj):
        """
        Возвращаем уровень компетенции в строковом формате.
        """
        return str(obj.competency_level)

    def get_color(self, obj):
        """
        Метод для вычисления цвета на основе уровня компетенции.
        """
        level = int(obj.competency_level)
        if level <= 33:
            return "red"
        elif 34 <= level <= 66:
            return "yellow"
        elif level >= 67:
            return "green"
        else:
            raise ValueError(
                f"Invalid competency level: {obj.competency_level}"
            )


class PeriodSerializer(serializers.Serializer):
    '''Сериализатор для периода.'''

    month = serializers.CharField()
    year = serializers.IntegerField()


class MetricDashboardEntrySerializer(serializers.Serializer):
    '''Сериализатор для метрик.'''

    period = PeriodSerializer()
    performance = serializers.CharField()


class TeamMetricResponseSerializer(serializers.Serializer):
    '''Сериализатор для метрик по команде.'''

    dashboard = MetricDashboardEntrySerializer(many=True)
    completionForToday = serializers.CharField()


class PeriodSerializer(serializers.Serializer):
    '''Сериализатор для периода.'''

    month = serializers.CharField()
    year = serializers.CharField()


class TeamEmployeeDashboardSerializer(serializers.Serializer):
    '''Сериализатор для метрик по команде.'''

    period = PeriodSerializer()
    numberOfEmployee = serializers.CharField()
    numberOfBusFactor = serializers.CharField()
    numberOfKeyPeople = serializers.CharField()


class CompetencySerializer(serializers.Serializer):
    '''Сериализатор для компетенции.'''

    competencyId = serializers.IntegerField(source='competency.id')
    skillDomen = serializers.SerializerMethodField()
    competencyName = serializers.CharField(source='competency.competency_name')
    plannedResult = serializers.CharField(source='planned_result')
    actualResult = serializers.SerializerMethodField()

    def get_skillDomen(self, obj):
        return obj.competency.competency_type.capitalize()

    def get_actualResult(self, obj):
        return f"{obj.actual_result:.1f}"


class SkillSerializer(serializers.ModelSerializer):
    skillId = serializers.IntegerField(source='id')
    skillName = serializers.CharField(source='skill_name')
    plannedResult = serializers.FloatField()
    actualResult = serializers.FloatField()

    class Meta:
        model = Skill
        fields = ['skillId', 'skillName', 'plannedResult', 'actualResult']


class TeamSkillSerializer(serializers.Serializer):
    numberOfEmployee = serializers.CharField(max_length=10)
    numberOfBusFactor = serializers.CharField(max_length=10)
    numberOfKeyPeople = serializers.CharField(max_length=10)


class IndividualSkillAverageSerializer(serializers.Serializer):
    skillDomen = serializers.CharField()
    skillId = serializers.IntegerField()
    skillName = serializers.CharField()
    plannedResult = serializers.FloatField()
    actualResult = serializers.FloatField()


class SkillLevelRequestSerializer(serializers.Serializer):
    skillId = serializers.IntegerField()
