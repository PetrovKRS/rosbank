from dataclasses import fields
from tabnanny import verbose

from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models


class Employee(AbstractUser):
    """ Модель сотрудника. """

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
    education = models.BooleanField(default=False)
    key_people = models.BooleanField(default=False)
    bus_factor = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Сотрудники'
        verbose_name_plural = 'Сотрудники'
        ordering = (
            'first_name',
        )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.pk})"


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

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
    )
    development_plan = models.ForeignKey(
        DevelopmentPlan,
        related_name='employee_development_plans',
        on_delete=models.CASCADE,
        verbose_name='План развития',
    )
    development_progress = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Процент развития',
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
        on_delete=models.CASCADE
    )
    engagement = models.ForeignKey(
        Engagement,
        related_name='employee_engagements',
        on_delete=models.CASCADE,
        verbose_name='Вовлеченность',
    )
    engagement_level = models.IntegerField(
        verbose_name='Уровень вовлеченности сотрудника',
    )

    class Meta:
        verbose_name = 'Вовлеченность сотрудника'
        verbose_name_plural = 'Вовлеченность сотрудников'
        ordering = (
            'engagement_level',
        )

    def __str__(self):
        return f"{self.employee} - {self.engagement}"
    

class KeyPeople(models.Model):
    """ Модель -Key People-. """

    key_people_name = models.CharField(
        max_length=255,
        verbose_name='Название key people',
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
    )
    key_people = models.ForeignKey(
        KeyPeople,
        related_name='employee_keys_peoples',
        on_delete=models.CASCADE,
        verbose_name='Key people',
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
        verbose_name='Количество сотрудников на обучении',
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
    )
    training_application = models.ForeignKey(
        TrainingApplication,
        related_name='employee_training_applications',
        on_delete=models.CASCADE,
        verbose_name='Заявка на обучение',
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
    """ # Модель -Bus Фактор-. """

    bus_factor_name = models.CharField(
        max_length=255,
        verbose_name='Название Bus фактора',
    )
    employee_count = models.IntegerField(
        default=0,
        verbose_name='Количество сотрудников с этим Bus фактором',
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
        on_delete=models.CASCADE
    )
    bus_factor = models.ForeignKey(
        BusFactor,
        related_name='employee_bus_factors',
        on_delete=models.CASCADE,
        verbose_name='Bus фактор',
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
    """ Модель -Класс-. """

    grade_name = models.CharField(
        max_length=255,
        verbose_name='Название класса',
    )

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'
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
    )
    grade = models.ForeignKey(
        Grade,
        related_name='employee_grades',
        on_delete=models.CASCADE,
        verbose_name='Класс',
    )

    class Meta:
        verbose_name = 'Класс сотрудника'
        verbose_name_plural = 'Классы сотрудников'
        ordering = (
            'grade',
        )

    def __str__(self):
        return f"{self.employee} - {self.grade}"


class KeySkill(models.Model):
    """ Модель -Ключевой навык-. """

    skill_name = models.CharField(
        max_length=255,
        verbose_name='Название ключевого навыка',
    )
    employee_count = models.IntegerField(
        default=0,
        verbose_name='Количество сотрудников с данным ключевым навыком',
    )

    class Meta:
        verbose_name = 'Ключевой навык'
        verbose_name_plural = 'Ключевые навыки'
        ordering = (
            'skill_name',
        )

    def __str__(self):
        return self.skill_name


class EmployeeKeySkill(models.Model):
    """ Модель -Ключевой навык сотрудника-. """

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
    )
    key_skill = models.ForeignKey(
        KeySkill,
        related_name='employee_key_skills',
        on_delete=models.CASCADE,
        verbose_name='Ключевой навык',
    )
    skill_level = models.CharField(
        max_length=255,
        verbose_name='Уровень ключевого навыка сотрудника',
    )

    class Meta:
        verbose_name = 'Ключевой навык сотрудника'
        verbose_name_plural = 'Ключевые навыки сотрудников'
        ordering = (
            'key_skill',
        )

    def __str__(self):
        return f"{self.employee} - {self.key_skill} ({self.skill_level})"


class Team(models.Model):
    """ Модель команды. """

    team_name = models.CharField(
        max_length=255,
        verbose_name='Название команды',
    )

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

    def __str__(self):
        return self.team_name


class EmployeeTeam(models.Model):
    """ Модель -Команда сотрудника-. """

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE
    )
    team = models.ForeignKey(
        Team,
        related_name='employee_teams',
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


class Position(models.Model):
    """ Модель -Должность-. """

    position_name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название должности',
    )
    grade_count = models.IntegerField(
        default=0,
        verbose_name='Количество грейдов, связанных с должностью'
    )

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
        ordering = (
            'position_name',
        )

    def __str__(self):
        return self.position_name


class EmployeePosition(models.Model):
    """ Модель -Должность сотрудника-. """

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )
    position = models.ForeignKey(
        Position,
        related_name='employee_positions',
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


class PositionCompetency(models.Model):
    """ Модель -Должность к компетенции-. """

    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
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


class TeamPosition(models.Model):
    """ Модель -Должность для команды-. """

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Должность для команды'
        verbose_name_plural = 'Должности для команд'
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
    )
    competency = models.ForeignKey(
        Competency,
        related_name='employee_competencies',
        on_delete=models.CASCADE,
        verbose_name='Компетенция',
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
        default=0)  # Количество сотрудников с данным навыком

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'
        ordering = (
            'skill_name',
        )

    def __str__(self):
        return self.skill_name


class EmployeeSkill(models.Model):
    """ Модель -Навык сотрудника-. """

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
    )
    skill = models.ForeignKey(
        Skill,
        related_name='employee_skills',
        on_delete=models.CASCADE,
        verbose_name='Навык',
    )
    skill_level = models.CharField(
        max_length=255,
        verbose_name='Уровень навыка сотрудника',
    )

    class Meta:
        verbose_name = 'Навык сотрудника'
        verbose_name_plural = 'Навыки сотрудников'
        ordering = (
            'skill',
        )

    def __str__(self):
        return f"{self.employee} - {self.skill} ({self.skill_level})"


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
        verbose_name='Сотрудник',
    )
    expected_skill = models.ForeignKey(
        ExpectedSkill,
        related_name='employee_expected_skills',
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
