from rest_framework import serializers
from users.models import ManagerTeam
from core.models import (
    DevelopmentPlan, EmployeeDevelopmentPlan, EmployeeEngagement,
    KeyPeople, EmployeeKeyPeople, TrainingApplication, EmployeeTrainingApplication,
    BusFactor, EmployeeBusFactor, Grade, EmployeeGrade, KeySkill, EmployeeKeySkill,
    Team, EmployeeTeam, Position, EmployeePosition, Competency, PositionCompetency,
    TeamPosition, EmployeeCompetency, Skill, EmployeeSkill, SkillForCompetency,
    ExpectedSkill, EmployeeExpectedSkill, SkillTypeEnum, Employee
)
from django.urls import reverse
from rest_framework.validators import UniqueTogetherValidator


# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Дополнительные данные, которые вы хотите включить в токен
#         token['email'] = user.email  # Например, добавление email в токен

#         return token




class WorkersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'id', 'employee_id', 'first_name', 'patronymic', 'position'
        )


class SkillSerializer(serializers.ModelSerializer):
    """ Сериализатор для навыков сотрудника. """

    skill = serializers.CharField(source='skill.skill_name')

    class Meta:
        model = EmployeeSkill
        fields = (
            'skill', 'skill_level'
        )


class CompetencySerializer(serializers.ModelSerializer):
    """ Сериализатор для компетенций сотрудника. """

    competency = serializers.CharField(source='competency.competency_name')

    class Meta:
        model = EmployeeCompetency
        fields = (
            'competency', 'competency_level'
        )
        
class TrainingApplicationSerializer(serializers.ModelSerializer):
    """ Сериализатор для заявок на обучение. """

    training_name = serializers.CharField(source='training_application.training_name')

    class Meta:
        model = EmployeeTrainingApplication
        fields = (
            'id', 'training_name',  # Указываем правильное поле через связь
        )
        

class AssesmentOfPotentionSerializer(serializers.Serializer):
    """ Сериализатор для оценки потенциала сотрудника. """
    assesmentLevel = serializers.CharField(source='grades.grade.grade_name')
    involvmentLevel = serializers.CharField(source='employee_engagements.engagement.engagement_name')
    

    

class EmployeeSerializer(serializers.ModelSerializer):
    """ Основной сериализатор для сотрудников. """

    worker = serializers.SerializerMethodField()
    # skills = SkillSerializer(many=True)
    # competencies = CompetencySerializer(
    #     source='employee_competencies', many=True
    # )
    position = serializers.CharField(
        source='positions.position.position_name', allow_null=True
    )
    grade = serializers.CharField(
        source='grades.grade.grade_name',
    )
    assesmentOfPotention = AssesmentOfPotentionSerializer(source='*') 

    key_people = serializers.SerializerMethodField()
    bus_factor = serializers.SerializerMethodField()
    education = TrainingApplicationSerializer(source='training_applications', many=True)
    skill = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            'id', 'position', 'worker', 'grade', 'key_people',
            'bus_factor', 'education', 'assesmentOfPotention', 'skill'
        )

    def get_worker(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    def get_skill(self, obj):
        """ Рассчитывает средний уровень навыков сотрудника. """
        skills = obj.skills.all()  # Получаем все связанные навыки
        if not skills:
            return 0  # Если навыков нет, возвращаем 0

        total_skill_level = sum(employee_skill.skill_level for employee_skill in skills)
        average_level = total_skill_level / len(skills)
        return average_level

    # Проверка наличия записи в EmployeeKeyPeople
    def get_key_people(self, obj):
        return EmployeeKeyPeople.objects.filter(employee=obj).exists()

    # Проверка наличия записи в EmployeeBusFactor
    def get_bus_factor(self, obj):
        return EmployeeBusFactor.objects.filter(employee=obj).exists()

    # Проверка наличия записи в EmployeeTrainingApplication (образование)
    def get_education(self, obj):
        return EmployeeTrainingApplication.objects.filter(employee=obj).exists()


# class DevelopmentPlanSerializer(serializers.ModelSerializer):
#     """ ."""
#
#     key_skill = serializers.CharField(source='key_skill.skill_name')
#
#     class Meta:
#         model = DevelopmentPlan
#         fields = (
#             'month', 'year', 'key_skill',
#         )


class MetricRequestSerializer(serializers.Serializer):
    employeeIds = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    startPeriod = serializers.DateField(required=True)
    endPeriod = serializers.DateField(required=True)



class IndividualDevelopmentPlanRequestSerializer(serializers.Serializer):

    startPeriod = serializers.DictField(
        child=serializers.CharField(),
        required=True
    )
    endPeriod = serializers.DictField(
        child=serializers.CharField(),
        required=True
    )


class IndividualDevelopmentPlanResponseSerializer(serializers.Serializer):
    dashboard = serializers.ListField(
        child=serializers.DictField()
    )
    completionForToday = serializers.CharField()


class TeamMetricsRequestSerializer(serializers.Serializer):
    startPeriod = serializers.DictField(
        child=serializers.CharField()
    )
    endPeriod = serializers.DictField(
        child=serializers.CharField()
    )


class PeriodSerializer(serializers.Serializer):
    month = serializers.CharField(max_length=20)
    year = serializers.IntegerField()

class SkillAssessmentRequestSerializer(serializers.Serializer):
    employeeIds = serializers.ListField(child=serializers.CharField())
    skillDomen = serializers.CharField(max_length=50)
    startPeriod = PeriodSerializer()
    endPeriod = PeriodSerializer()

class SkillDataSerializer(serializers.Serializer):
    skillId = serializers.IntegerField()
    skillName = serializers.CharField(max_length=100)
    assesment = serializers.IntegerField()

class TeamSkillAssessmentResponseSerializer(serializers.Serializer):
    period = PeriodSerializer()
    skillsData = serializers.ListField(child=SkillDataSerializer())



class SkillDomenRequestSerializer(serializers.Serializer):
    skillDomen = serializers.ChoiceField(
        choices=SkillTypeEnum.choices(),
        help_text="Тип навыка: hard или soft"
    )
    
    
class CompetencySerializer(serializers.Serializer):
    competencyId = serializers.IntegerField()
    skillDomen = serializers.CharField()
    competencyName = serializers.CharField()
    plannedResult = serializers.FloatField()
    actualResult = serializers.FloatField()
    

class CompetencyLevelRequestSerializer(serializers.Serializer):
    competencyId = serializers.IntegerField()
    

class MetricResponseSerializer(serializers.Serializer):
    period = serializers.DictField()
    performance = serializers.CharField()
    
    
class TeamMetricsResponseSerializer(serializers.Serializer):
    period = serializers.DictField(child=serializers.CharField())
    numberOfEmployee = serializers.CharField()
    numberOfBusFactor = serializers.CharField()
    numberOfKeyPeople = serializers.CharField()
    
    
class EmployeeCompetencySerializer(serializers.ModelSerializer):
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
        return obj.competency.competency_type.capitalize()

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
            raise ValueError(f"Invalid competency level: {obj.competency_level}")
        

class PeriodSerializer(serializers.Serializer):
    month = serializers.CharField()
    year = serializers.IntegerField()

class MetricDashboardEntrySerializer(serializers.Serializer):
    period = PeriodSerializer()
    performance = serializers.CharField()

class TeamMetricResponseSerializer(serializers.Serializer):
    dashboard = MetricDashboardEntrySerializer(many=True)
    completionForToday = serializers.CharField()
    
class PeriodSerializer(serializers.Serializer):
    month = serializers.CharField()
    year = serializers.CharField()

class TeamEmployeeDashboardSerializer(serializers.Serializer):
    period = PeriodSerializer()
    numberOfEmployee = serializers.CharField()
    numberOfBusFactor = serializers.CharField()
    numberOfKeyPeople = serializers.CharField()
    
    
class CompetencySerializer(serializers.Serializer):
    competencyId = serializers.IntegerField(source='competency.id')
    skillDomen = serializers.SerializerMethodField()
    competencyName = serializers.CharField(source='competency.competency_name')
    plannedResult = serializers.CharField(source='planned_result')
    actualResult = serializers.SerializerMethodField()

    def get_skillDomen(self, obj):
        # Возвращаем тип компетенции с заглавной буквы
        return obj.competency.competency_type.capitalize()

    def get_actualResult(self, obj):
        return f"{obj.actual_result:.1f}"