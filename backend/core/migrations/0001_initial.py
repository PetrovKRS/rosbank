# Generated by Django 4.2 on 2024-10-07 13:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BusFactor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "bus_factor_name",
                    models.CharField(
                        max_length=255, verbose_name="Название Bus фактора"
                    ),
                ),
                (
                    "employee_count",
                    models.IntegerField(
                        default=0,
                        verbose_name="Количество сотрудников с этим Bus фактором",
                    ),
                ),
            ],
            options={
                "verbose_name": "Bus Фактор",
                "verbose_name_plural": "Bus Факторы",
                "ordering": ("bus_factor_name",),
            },
        ),
        migrations.CreateModel(
            name="Competency",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "competency_name",
                    models.CharField(
                        max_length=255, verbose_name="Название компетенции"
                    ),
                ),
                (
                    "employee_count",
                    models.IntegerField(
                        default=0,
                        verbose_name="Количество сотрудников с данной компетенцией",
                    ),
                ),
            ],
            options={
                "verbose_name": "Компетенция",
                "verbose_name_plural": "Компетенции",
                "ordering": ("competency_name",),
            },
        ),
        migrations.CreateModel(
            name="DevelopmentPlan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "plan_name",
                    models.CharField(
                        max_length=255, unique=True, verbose_name="Название плана"
                    ),
                ),
                (
                    "employee_count",
                    models.IntegerField(
                        default=0, verbose_name="Кол-во сотрудников с планом развития"
                    ),
                ),
            ],
            options={
                "verbose_name": "План развития",
                "verbose_name_plural": "Планы развития",
                "ordering": ("plan_name",),
            },
        ),
        migrations.CreateModel(
            name="Engagement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "engagement_name",
                    models.CharField(
                        max_length=255, verbose_name="Название вовлеченности"
                    ),
                ),
                (
                    "employee_count",
                    models.IntegerField(
                        default=0, verbose_name="Количество вовлеченных сотрудников"
                    ),
                ),
            ],
            options={
                "verbose_name": "Вовлеченность",
                "verbose_name_plural": "Вовлеченности",
                "ordering": ("engagement_name",),
            },
        ),
        migrations.CreateModel(
            name="ExpectedSkill",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "expected_skill_name",
                    models.CharField(
                        max_length=255, verbose_name="Название ожидаемого навыка"
                    ),
                ),
                (
                    "employee_count",
                    models.IntegerField(
                        default=0,
                        verbose_name="Количество сотрудников с данным ожидаемым навыком",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ожидаемый навык",
                "verbose_name_plural": "Ожидаемые навыки",
                "ordering": ("expected_skill_name",),
            },
        ),
        migrations.CreateModel(
            name="Grade",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "grade_name",
                    models.CharField(max_length=255, verbose_name="Название класса"),
                ),
            ],
            options={
                "verbose_name": "Класс",
                "verbose_name_plural": "Классы",
                "ordering": ("grade_name",),
            },
        ),
        migrations.CreateModel(
            name="KeyPeople",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "key_people_name",
                    models.CharField(
                        max_length=255, verbose_name="Название key people"
                    ),
                ),
                (
                    "employee_count",
                    models.IntegerField(
                        default=0, verbose_name="Количество сотрудников Key People"
                    ),
                ),
            ],
            options={
                "verbose_name": "Вовлеченность сотрудника",
                "verbose_name_plural": "Вовлеченность сотрудников",
                "ordering": ("key_people_name",),
            },
        ),
        migrations.CreateModel(
            name="KeySkill",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "skill_name",
                    models.CharField(
                        max_length=255, verbose_name="Название ключевого навыка"
                    ),
                ),
                (
                    "employee_count",
                    models.IntegerField(
                        default=0,
                        verbose_name="Количество сотрудников с данным ключевым навыком",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ключевой навык",
                "verbose_name_plural": "Ключевые навыки",
                "ordering": ("skill_name",),
            },
        ),
        migrations.CreateModel(
            name="Position",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "position_name",
                    models.CharField(
                        max_length=255, unique=True, verbose_name="Название должности"
                    ),
                ),
                (
                    "grade_count",
                    models.IntegerField(
                        default=0,
                        verbose_name="Количество грейдов, связанных с должностью",
                    ),
                ),
            ],
            options={
                "verbose_name": "Должность",
                "verbose_name_plural": "Должности",
                "ordering": ("position_name",),
            },
        ),
        migrations.CreateModel(
            name="Skill",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "skill_name",
                    models.CharField(max_length=255, verbose_name="Название навыка"),
                ),
                ("employee_count", models.IntegerField(default=0)),
            ],
            options={
                "verbose_name": "Навык",
                "verbose_name_plural": "Навыки",
                "ordering": ("skill_name",),
            },
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "team_name",
                    models.CharField(max_length=255, verbose_name="Название команды"),
                ),
            ],
            options={
                "verbose_name": "Команда",
                "verbose_name_plural": "Команды",
            },
        ),
        migrations.CreateModel(
            name="TrainingApplication",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "training_name",
                    models.CharField(max_length=255, verbose_name="Название обучения"),
                ),
                (
                    "employee_count",
                    models.IntegerField(
                        default=0, verbose_name="Количество сотрудников на обучении"
                    ),
                ),
            ],
            options={
                "verbose_name": "Заявка на обучение",
                "verbose_name_plural": "Заявки на обучение",
                "ordering": ("training_name",),
            },
        ),
        migrations.CreateModel(
            name="TeamPosition",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "position",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.position"
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.team"
                    ),
                ),
            ],
            options={
                "verbose_name": "Должность для команды",
                "verbose_name_plural": "Должности для команд",
                "ordering": ("team",),
            },
        ),
        migrations.CreateModel(
            name="SkillForCompetency",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "competency",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.competency",
                    ),
                ),
                (
                    "skill",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.skill"
                    ),
                ),
            ],
            options={
                "verbose_name": "Навык для компетенции",
                "verbose_name_plural": "Навыки для компетенций",
            },
        ),
        migrations.CreateModel(
            name="PositionCompetency",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "competency",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.competency",
                    ),
                ),
                (
                    "position",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="competencies",
                        to="core.position",
                    ),
                ),
            ],
            options={
                "verbose_name": "Должность к компетенции",
                "verbose_name_plural": "Должности к компетенциям",
            },
        ),
        migrations.CreateModel(
            name="EmployeeTrainingApplication",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "add_date",
                    models.DateField(
                        auto_now_add=True,
                        db_index=True,
                        verbose_name="Дата добавления заявки на обучение",
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="training_applications",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "training_application",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.trainingapplication",
                        verbose_name="Заявка на обучение",
                    ),
                ),
            ],
            options={
                "verbose_name": "Заявка на обучение сотрудника",
                "verbose_name_plural": "Заявки на обучение сотрудников",
                "ordering": ("training_application",),
            },
        ),
        migrations.CreateModel(
            name="EmployeeTeam",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "employee",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="teams",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.team",
                        verbose_name="Команда",
                    ),
                ),
            ],
            options={
                "verbose_name": "Команда сотрудника",
                "verbose_name_plural": "Команды сотрудников",
                "ordering": ("team",),
            },
        ),
        migrations.CreateModel(
            name="EmployeeSkill",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "skill_level",
                    models.CharField(
                        max_length=255, verbose_name="Уровень навыка сотрудника"
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="skills",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "skill",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.skill",
                        verbose_name="Навык",
                    ),
                ),
            ],
            options={
                "verbose_name": "Навык сотрудника",
                "verbose_name_plural": "Навыки сотрудников",
                "ordering": ("skill",),
            },
        ),
        migrations.CreateModel(
            name="EmployeePosition",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="positions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "position",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.position",
                        verbose_name="Должность",
                    ),
                ),
            ],
            options={
                "verbose_name": "Должность сотрудника",
                "verbose_name_plural": "Должности сотрудников",
                "ordering": ("position",),
            },
        ),
        migrations.CreateModel(
            name="EmployeeKeySkill",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "skill_level",
                    models.CharField(
                        max_length=255,
                        verbose_name="Уровень ключевого навыка сотрудника",
                    ),
                ),
                (
                    "add_date",
                    models.DateField(
                        auto_now_add=True,
                        db_index=True,
                        verbose_name="Дата добавления ключевого навыка сотрудника",
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="key_skills",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "key_skill",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.keyskill",
                        verbose_name="Ключевой навык",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ключевой навык сотрудника",
                "verbose_name_plural": "Ключевые навыки сотрудников",
                "ordering": ("key_skill",),
            },
        ),
        migrations.CreateModel(
            name="EmployeeKeyPeople",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "add_date",
                    models.DateField(
                        auto_now_add=True,
                        db_index=True,
                        verbose_name="Дата добавления ключевого сотрудника",
                    ),
                ),
                (
                    "employee",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="keys_people",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "key_people",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.keypeople",
                        verbose_name="Key people",
                    ),
                ),
            ],
            options={
                "verbose_name": "Key People сотрудника",
                "verbose_name_plural": "Key People сотрудников",
                "ordering": ("key_people",),
            },
        ),
        migrations.CreateModel(
            name="EmployeeGrade",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "employee",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="grades",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "grade",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.grade",
                        verbose_name="Класс",
                    ),
                ),
            ],
            options={
                "verbose_name": "Класс сотрудника",
                "verbose_name_plural": "Классы сотрудников",
                "ordering": ("grade",),
            },
        ),
        migrations.CreateModel(
            name="EmployeeExpectedSkill",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="expected_skills",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "expected_skill",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.expectedskill",
                        verbose_name="Ожидаемый навык",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ожидаемый навык сотрудника",
                "verbose_name_plural": "Ожидаемые навыки сотрудниов",
                "ordering": ("expected_skill",),
            },
        ),
        migrations.CreateModel(
            name="EmployeeEngagement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "engagement_level",
                    models.IntegerField(
                        verbose_name="Уровень вовлеченности сотрудника"
                    ),
                ),
                (
                    "add_date",
                    models.DateField(
                        auto_now_add=True,
                        db_index=True,
                        verbose_name="Дата вовлечения сотрудника",
                    ),
                ),
                (
                    "employee",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="employee_engagements",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "engagement",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.engagement",
                        verbose_name="Вовлеченность",
                    ),
                ),
            ],
            options={
                "verbose_name": "Вовлеченность сотрудника",
                "verbose_name_plural": "Вовлеченность сотрудников",
                "ordering": ("engagement_level",),
            },
        ),
        migrations.CreateModel(
            name="EmployeeDevelopmentPlan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "development_progress",
                    models.DecimalField(
                        decimal_places=2, max_digits=5, verbose_name="Процент развития"
                    ),
                ),
                (
                    "add_date",
                    models.DateField(
                        auto_now_add=True,
                        db_index=True,
                        verbose_name="Дата добавления сотрудника в план развития",
                    ),
                ),
                (
                    "development_plan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.developmentplan",
                        verbose_name="План развития",
                    ),
                ),
                (
                    "employee",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="development_plans",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "План развития сотрудника",
                "verbose_name_plural": "Планы развития сотрудников",
                "ordering": ("development_plan",),
            },
        ),
        migrations.CreateModel(
            name="EmployeeCompetency",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "competency_level",
                    models.CharField(
                        max_length=255, verbose_name="Уровень компетенции сотрудника"
                    ),
                ),
                (
                    "competency",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.competency",
                        verbose_name="Компетенция",
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="employee_competencies",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Компетенция сотрудника",
                "verbose_name_plural": "Компетенции сотрудников",
                "ordering": ("competency",),
            },
        ),
        migrations.CreateModel(
            name="EmployeeBusFactor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "add_date",
                    models.DateField(
                        auto_now_add=True,
                        db_index=True,
                        verbose_name="Дата добавления bud-фактора сотрудника",
                    ),
                ),
                (
                    "bus_factor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.busfactor",
                        verbose_name="Bus фактор",
                    ),
                ),
                (
                    "employee",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bus_factors",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Bus Фактор сотрудника",
                "verbose_name_plural": "Bus Факторы сотрудников",
                "ordering": ("bus_factor",),
            },
        ),
        migrations.CreateModel(
            name="CompetencyForExpectedSkill",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "competency",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.competency",
                    ),
                ),
                (
                    "expected_skill",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.expectedskill",
                    ),
                ),
            ],
            options={
                "verbose_name": "Компетенция для ожидаемого навыка",
                "verbose_name_plural": "Компетенции для ожидаемых навыков",
            },
        ),
        migrations.AddConstraint(
            model_name="skillforcompetency",
            constraint=models.UniqueConstraint(
                fields=("skill", "competency"), name="unique_skill_competency"
            ),
        ),
        migrations.AddConstraint(
            model_name="positioncompetency",
            constraint=models.UniqueConstraint(
                fields=("position", "competency"), name="unique_position_competency"
            ),
        ),
        migrations.AddConstraint(
            model_name="competencyforexpectedskill",
            constraint=models.UniqueConstraint(
                fields=("expected_skill", "competency"),
                name="unique_expected_skill_competency",
            ),
        ),
    ]
