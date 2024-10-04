from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models


class Employee(AbstractUser):
    """ Модель сотрудника. """

    employee_id = models.CharField(
        max_length=100,
        unique=True,
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

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"


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
        on_delete=models.CASCADE,
    )
    development_progress = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Процент развития',
    )

    def __str__(self):
        return f"{self.employee} - {self.development_plan}"
    

class Engagement(models.Model):
    """ Модель -Вовлеченность-. """

    engagement_name = models.CharField(
        max_length=255,
        verbose_name='Название вовлеченности',
    )
    employee_count = models.IntegerField(
        default=0,
        verbose_name='Количество вовлеченных сотрудников',
    )

    def __str__(self):
        return self.engagement_name


class EmployeeEngagement(models.Model):
    """ Модель -Вовлеченность сотрудника-. """

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE
    )
    engagement = models.ForeignKey(
        Engagement,
        on_delete=models.CASCADE,
    )
    engagement_level = models.IntegerField(
        verbose_name='Уровень вовлеченности сотрудника',
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
        on_delete=models.CASCADE,
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
        on_delete=models.CASCADE,
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
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.employee} - {self.bus_factor}"
    

class Grade(models.Model):

    grade_name = models.CharField(
        max_length=255,
        verbose_name='Название грейда',
    )

    def __str__(self):
        return self.grade_name


class EmployeeGrade(models.Model):
    """ Модель -Грейд сотрудника-. """

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
    )
    grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE
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
        on_delete=models.CASCADE,
    )
    skill_level = models.CharField(
        max_length=255,
        verbose_name='Уровень ключевого навыка сотрудника',
    )

    def __str__(self):
        return f"{self.employee} - {self.key_skill} ({self.skill_level})"


class Team(models.Model):
    """ Модель команды. """

    team_name = models.CharField(
        max_length=255,
        verbose_name='Название команды',
    )

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
        on_delete=models.CASCADE,
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
        on_delete=models.CASCADE
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
        on_delete=models.CASCADE,
    )
    competency_level = models.CharField(
        max_length=255,
        verbose_name='Уровень компетенции сотрудника',
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
        on_delete=models.CASCADE,
    )
    skill_level = models.CharField(
        max_length=255,
        verbose_name='Уровень навыка сотрудника',
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

    def __str__(self):
        return self.expected_skill_name


class EmployeeExpectedSkill(models.Model):
    """ Модель -Ожидаемый навык сотрудника-. """

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
    )
    expected_skill = models.ForeignKey(
        ExpectedSkill,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.employee} - {self.expected_skill} ({self.skill_level})"


class CompetencyForExpectedSkill(models.Model):
    """ Модель -Компетенция для ожидаемого навыка-. """

    expected_skill = models.OneToOneField(
        ExpectedSkill,
        on_delete=models.CASCADE,
    )
    competency = models.ForeignKey(Competency, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.expected_skill} - {self.competency}"
