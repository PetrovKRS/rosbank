# Generated by Django 4.2 on 2024-10-10 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0012_competency_competency_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="employeecompetency",
            name="actual_result",
            field=models.FloatField(
                default=0.0, verbose_name="Фактическая оценка"
            ),
        ),
        migrations.AddField(
            model_name="employeecompetency",
            name="planned_result",
            field=models.FloatField(
                default=0.0, verbose_name="Плановая оценка"
            ),
        ),
    ]
