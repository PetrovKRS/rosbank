# Generated by Django 4.2 on 2024-10-09 18:38

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_skill_skill_type_alter_skill_employee_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='skill_type',
            field=models.CharField(
                choices=[('hard', 'Hard'), ('soft', 'Soft')],
                default=core.models.SkillTypeEnum['HARD'],
                max_length=4,
                verbose_name='Тип навыка',
            ),
        ),
    ]
