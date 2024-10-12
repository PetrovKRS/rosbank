from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from core.models import (
    EmployeeSkill, Skill, EmployeeCompetency, Competency
)


# Сигнал на создание или удаление навыка сотрудника
@receiver([post_save, post_delete], sender=EmployeeSkill)
def update_employee_count(sender, instance, **kwargs):
    skill = instance.skill
    # Подсчет количества сотрудников с данным навыком
    skill.employee_count = EmployeeSkill.objects.filter(skill=skill).count()
    skill.save()


# Сигнал на создание или удаление компетенции сотрудника
@receiver([post_save, post_delete], sender=EmployeeCompetency)
def update_employee_competency_count(sender, instance, **kwargs):
    competency = instance.competency
    # Подсчет количества сотрудников с данной компетенцией
    competency.employee_count = EmployeeCompetency.objects.filter(competency=competency).count()
    competency.save()
