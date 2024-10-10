from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.formats import date_format
from django.views.decorators.http import condition
from django_filters.utils import verbose_field_name

from users.models import ManagerTeam
import uuid

class Employee(models.Model):
    """ Модель сотрудника. """

    employee_id = models.CharField(
        max_length=100,
        unique=True,
        editable=False,  # Поле не должно редактироваться
        default=uuid.uuid4,  # Генерация уникального идентификатора
    )
    first_name = models.CharField(
        max_length=100,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='Фамилия',
    )
    email = models.EmailField(
        max_length=100,
        unique=True,
        verbose_name='E-mail'
    )
    status = models.CharField(
        max_length=50
    )  # E.g., completed, in-progress
    registration_date = models.DateField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата регистрации сотрудника'
    )
    last_login_date = models.DateField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата последнего входа сотрудника',
    )

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = (
            'first_name',
            'last_name',
        )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"


class AssesmentSkill(models.Model):
    """ Оценка навыка. """

    assesmentskill_name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название оценки',
    )

    class Meta:
        verbose_name = 'Оценка навыка'
        verbose_name_plural = 'Оценки навыков'
        ordering = (
            'assesmentskill_name',
        )


class EmployeeAssesmentSkill(models.Model):
    """ Модель -Оценка сотрудника-. """

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='assesments_skills',
    )
    avg_assesment_skill = models.ForeignKey(
        AssesmentSkill,
        on_delete=models.CASCADE,
        verbose_name='Оценка навыка сотрудника',
    )
    assesment = models.IntegerField(
        default=0,
        verbose_name='Оценка навыка сотрудника',
    )

    class Meta:
        verbose_name = 'Оценка навыка сотрудника'
        verbose_name_plural = 'Оценки навыков сотрудников'
        ordering = (
        'employee',
    )


class DevelopmentPlan(models.Model):
    """ Модель -План развития-."""

    plan_name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название плана',
    )
    employee_count = models.IntegerField(
        default=0,
        verbose_name='Кол-во сотрудников с планом развития',
    )


    class Meta:
        verbose_name = 'План развития'
        verbose_name_plural = 'Планы развития'
        ordering = (
            'plan_name',
        )

    def __str__(self):
        return self.plan_name


class EmployeeDevelopmentPlan(models.Model):
    """ Модель -План развития сотрудника-. """

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='development_plans',
    )
    development_plan = models.ForeignKey(
        DevelopmentPlan,
        on_delete=models.CASCADE,
        verbose_name='План развития',
    )
    performance_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Процент развития',
    )
    start_date = models.DateField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления сотрудника в план развития',
    )
    end_date = models.DateField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата завершения плана развития сотрудника',
    )
    development_assesment = models.IntegerField(
        default=0,
        verbose_name='Оценка развития сотрудника',
    )

    class Meta:
        verbose_name = 'План развития сотрудника'
        verbose_name_plural = 'Планы развития сотрудников'
        ordering = (
            'development_plan',
        )

    def __str__(self):
        return f"{self.employee} - {self.development_plan}"
    

class Engagement(models.Model):
    """ Модель -Вовлеченность-. """

    engagement_name = models.CharField(
        max_length=255,
        verbose_name='Название вовлеченности',
    )
    def __str__(self):
        return self.engagement_name

    employee_count = models.IntegerField(
        default=0,
        verbose_name='Количество вовлеченных сотрудников',
    )

    class Meta:
        verbose_name = 'Вовлеченность'
        verbose_name_plural = 'Вовлеченности'
        ordering = (
            'engagement_name',
        )


class EmployeeEngagement(models.Model):
    """ Модель -Вовлеченность сотрудника-. """

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name='employee_engagements',
    )
    engagement = models.ForeignKey(
        Engagement,
        on_delete=models.CASCADE,
        verbose_name='Вовлеченность',
    )
    performance_score = models.IntegerField(
        verbose_name='Уровень вовлеченности сотрудника',
    )
    start_date = models.DateField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Начальная дата',
    )
    end_date = models.DateField(
        db_index=True,
        verbose_name='Конечная дата',
    )

    class Meta:
        verbose_name = 'Вовлеченность сотрудника'
        verbose_name_plural = 'Вовлеченность сотрудников'
        ordering = (
            'performance_score',
        )

    def __str__(self):
        return f"{self.employee} - {self.engagement}"
    

class KeyPeople(models.Model):
    """ Модель -Key People-. """

    key_people_name = models.CharField(
        max_length=255,
        verbose_name='Имя key people',
    )
    employee_count = models.IntegerField(
        default=0,
        verbose_name='Количество сотрудников Key People'
    )

    class Meta:
        verbose_name = 'Вовлеченность сотрудника'
        verbose_name_plural = 'Вовлеченность сотрудников'
        ordering = (
            'key_people_name',
        )

    def __str__(self):
        return self.key_people_name


class EmployeeKeyPeople(models.Model):
    """ Модель -Key People сотрудника-. """

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name='keys_people',
    )
    key_people = models.ForeignKey(
        KeyPeople,
        on_delete=models.CASCADE,
        verbose_name='Key people',
    )
    start_date = models.DateField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Начальная дата',
    )
    end_date = models.DateField(
        db_index=True,
        verbose_name='Конечная дата',
    )

    class Meta:
        verbose_name = 'Key People сотрудника'
        verbose_name_plural = 'Key People сотрудников'
        ordering = (
            'key_people',
        )

    def __str__(self):
        return f"{self.employee} - {self.key_people}"
    

class TrainingApplication(models.Model):
    """ Модель -Заявка на обучение-. """

    training_name = models.CharField(
        max_length=255,
        verbose_name='Название обучения',
    )
    employee_count = models.IntegerField(
        default=0,
        verbose_name='Количество сотрудников на обучение',
    )

    class Meta:
        verbose_name = 'Заявка на обучение'
        verbose_name_plural = 'Заявки на обучение'
        ordering = (
            'training_name',
        )

    def __str__(self):
        return self.training_name


class EmployeeTrainingApplication(models.Model):
    """ Модель -Заявка на обучение сотрудника-. """

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='training_applications',
    )
    training_application = models.ForeignKey(
        TrainingApplication,
        on_delete=models.CASCADE,
        verbose_name='Название обучения',
    )

    class Meta:
        verbose_name = 'Заявка на обучение сотрудника'
        verbose_name_plural = 'Заявки на обучение сотрудников'
        ordering = (
            'training_application',
        )

    def __str__(self):
        return f"{self.employee} - {self.training_application}"    
    

class BusFactor(models.Model):
    """ Модель -Bus Фактор-. """

    bus_factor_name = models.CharField(
        max_length=255,
        verbose_name='Название Bus фактора',
    )
    employee_count = models.IntegerField(
        default=0,
        verbose_name='Количество сотрудников Bus фактор',
    )

    class Meta:
        verbose_name = 'Bus Фактор'
        verbose_name_plural = 'Bus Факторы'
        ordering = (
            'bus_factor_name',
        )

    def __str__(self):
        return self.bus_factor_name


class EmployeeBusFactor(models.Model):
    """ Модель -Bus Фактор сотрудника-. """

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name='bus_factors',
    )
    bus_factor = models.ForeignKey(
        BusFactor,
        on_delete=models.CASCADE,
        verbose_name='Bus фактор',
    )
    start_date = models.DateField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Начальная дата',
    )
    end_date = models.DateField(
        db_index=True,
        verbose_name='Конечная дата',
    )

    class Meta:
        verbose_name = 'Bus Фактор сотрудника'
        verbose_name_plural = 'Bus Факторы сотрудников'
        ordering = (
            'bus_factor',
        )

    def __str__(self):
        return f"{self.employee} - {self.bus_factor}"
    

class Grade(models.Model):
    """ Модель -Grade-. """

    grade_name = models.CharField(
        max_length=255,
        verbose_name='Название грейда',
    )

    class Meta:
        verbose_name = 'Грейд'
        verbose_name_plural = 'Грейды'
        ordering = (
            'grade_name',
        )

    def __str__(self):
        return self.grade_name


class EmployeeGrade(models.Model):
    """ Модель -Класс сотрудника-. """

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name='grades',
    )
    grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE,
        verbose_name='Грейд',
    )

    class Meta:
        verbose_name = 'Грейд сотрудника'
        verbose_name_plural = 'Грейды сотрудников'
        ordering = (
            'grade',
        )

    def __str__(self):
        return f"{self.employee} - {self.grade}"


class Team(models.Model):
    """ Модель команды. """

    team_name = models.CharField(
        max_length=255,
        verbose_name='Название команды',
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='Слаг команды',
    )

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

    def __str__(self):
        return self.team_name


class EmployeeTeam(models.Model):
    """ Модель -Команда сотрудника-. """

    manager  = models.ForeignKey(
        ManagerTeam,
        on_delete=models.CASCADE,
        related_name='teams',
        verbose_name='Менеджер команды',
    )
    employee = models.ManyToManyField(
        Employee,
        related_name='teams',
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        verbose_name='Команда',
    )

    class Meta:
        verbose_name = 'Команда сотрудника'
        verbose_name_plural = 'Команды сотрудников'
        ordering = (
            'team',
        )

    def __str__(self):
        return f"{self.employee} - {self.team}"


class Specialization(models.Model):
    """ Модель -Специальность-. """

    specialization_name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название специальности',
    )
    grade_count = models.IntegerField(
        default=0,
        verbose_name='Количество грейдов, связанных со специальностью'
    )

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
        ordering = (
            'position_name',
        )

    def __str__(self):
        return self.position_name


class EmployeeSpecialization(models.Model):
    """ Модель -Специальность сотрудника-. """

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='specializations',
    )
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.CASCADE,
        verbose_name='Должность',
    )

    class Meta:
        verbose_name = 'Должность сотрудника'
        verbose_name_plural = 'Должности сотрудников'
        ordering = (
            'position',
        )

    def __str__(self):
        return f"{self.employee} - {self.position}"


class Competency(models.Model):
    """ Модель -Компетенция-. """

    competency_name = models.CharField(
        max_length=255,
        verbose_name='Название компетенции',
    )
    competency_domen = models.CharField(
        max_length=255,
        verbose_name='Домен компетенции',
    )
    employee_count = models.IntegerField(
        default=0,
        verbose_name='Количество сотрудников с данной компетенцией'
    )

    class Meta:
        verbose_name = 'Компетенция'
        verbose_name_plural = 'Компетенции'
        ordering = (
            'competency_name',
        )

    def __str__(self):
        return self.competency_name


class CompetencySpecialization(models.Model):
    """ Модель -компетенция к специальности-. """

    specialization = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name='competencies',
    )
    competency = models.ForeignKey(
        Competency,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Должность к компетенции'
        verbose_name_plural = 'Должности к компетенциям'
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'position',
                    'competency'
                ),
                name='unique_position_competency'
            ),
        )

    def __str__(self):
        return f"{self.position} - {self.competency}"


class TeamSpecialization(models.Model):
    """ Модель -Должность для команды-. """

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
    )
    specialization = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Специальность для команды'
        verbose_name_plural = 'Специальности для команд'
        ordering = (
            'team',
        )

    def __str__(self):
        return f"{self.team} - {self.position}"


class EmployeeCompetency(models.Model):
    """ Модель -Компетенция сотрудника-. """

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='employee_competencies',
    )
    competency = models.ForeignKey(
        Competency,
        on_delete=models.CASCADE,
        verbose_name='Компетенция',
    )
    planned_assessment = models.IntegerField(
        default=0,
        verbose_name='Плановая оценка',
    )
    actual_assessment = models.IntegerField(
        default=0,
        verbose_name='Фактическая оценка',
    )
    competency_level = models.CharField(
        max_length=255,
        verbose_name='Уровень компетенции сотрудника',
    )

    class Meta:
        verbose_name = 'Компетенция сотрудника'
        verbose_name_plural = 'Компетенции сотрудников'
        ordering = (
            'competency',
        )

    def __str__(self):
        return f"{self.employee} - {self.competency} ({self.competency_level})"
    

class Skill(models.Model):
    """ Модель -Навык-. """

    skill_name = models.CharField(
        max_length=255,
        verbose_name='Название навыка',
    )
    employee_count = models.IntegerField(
        default=0,
        verbose_name='Количество сотрудников с данным навыком',
    )

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'
        ordering = (
            'skill_name',
        )

    def __str__(self):
        return f'{self.skill_name} ({self.skill_type})'


class EmployeeSkill(models.Model):
    """ Модель -Навык сотрудника-. """

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='skills',
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        verbose_name='Навык',
    )
    skill_level = models.IntegerField(
        default=0,
        verbose_name='Уровень навыка сотрудника',
    )
    planned_assessment_skill = models.IntegerField(
        default=0,
        verbose_name='Плановая оценка навыка',
    )
    actual_assessment_skill = models.IntegerField(
        default=0,
        verbose_name='Фактическая оценка навыка',
    )
    start_date = models.DateField(
        auto_now_add=True,
        verbose_name='Начальная дата',
    )
    end_date = models.DateField(
        db_index=True,
        verbose_name='Конечная дата',
    )


    class Meta:
        verbose_name = 'Навык сотрудника'
        verbose_name_plural = 'Навыки сотрудников'
        ordering = (
            'skill',
        )

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.skill.skill_name} ({self.skill_level})"


class SkillForCompetency(models.Model):
    """ Модель -Навык для компетенции-. """

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
    )
    competency = models.ForeignKey(
        Competency,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Навык для компетенции'
        verbose_name_plural = 'Навыки для компетенций'
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'skill',
                    'competency'
                ),
                name='unique_skill_competency'
            ),
        )

    def __str__(self):
        return f"{self.skill} - {self.competency}"
    

class ExpectedSkill(models.Model):
    """ Модель -Ожидаемый навык-. """

    expected_skill_name = models.CharField(
        max_length=255,
        verbose_name='Название ожидаемого навыка',
    )
    employee_count = models.IntegerField(
        default=0,
        verbose_name='Количество сотрудников с данным ожидаемым навыком',
    )

    class Meta:
        verbose_name = 'Ожидаемый навык'
        verbose_name_plural = 'Ожидаемые навыки'
        ordering = (
            'expected_skill_name',
        )

    def __str__(self):
        return self.expected_skill_name


class EmployeeExpectedSkill(models.Model):
    """ Модель -Ожидаемый навык сотрудника-. """

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='expected_skills',
    )
    expected_skill = models.ForeignKey(
        ExpectedSkill,
        on_delete=models.CASCADE,
        verbose_name='Ожидаемый навык',
    )

    class Meta:
        verbose_name = 'Ожидаемый навык сотрудника'
        verbose_name_plural = 'Ожидаемые навыки сотрудниов'
        ordering = (
            'expected_skill',
        )

    def __str__(self):
        return f"{self.employee} - {self.expected_skill} ({self.skill_level})"


class CompetencyForExpectedSkill(models.Model):
    """ Модель -Компетенция для ожидаемого навыка-. """

    expected_skill = models.OneToOneField(
        ExpectedSkill,
        on_delete=models.CASCADE,
    )
    competency = models.ForeignKey(
        Competency,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Компетенция для ожидаемого навыка'
        verbose_name_plural = 'Компетенции для ожидаемых навыков'
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'expected_skill',
                    'competency'
                ),
                name='unique_expected_skill_competency'
            ),
        )

    def __str__(self):
        return f"{self.expected_skill} - {self.competency}"

