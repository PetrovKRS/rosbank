from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from core.models import (
    EmployeeSkill, Skill, EmployeeCompetency, Competency,
    EmployeeBusFactor, EmployeeKeyPeople,
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


# Сигнал для обновления employee_count при добавлении записи EmployeeBusFactor
@receiver(post_save, sender=EmployeeBusFactor)
def update_employee_count_on_save(sender, instance, created, **kwargs):
    if created:
        bus_factor = instance.bus_factor
        bus_factor.employee_count = EmployeeBusFactor.objects.filter(bus_factor=bus_factor).count()
        bus_factor.save()


# Сигнал для обновления employee_count при удалении записи EmployeeBusFactor
@receiver(post_delete, sender=EmployeeBusFactor)
def update_employee_count_on_delete(sender, instance, **kwargs):
    bus_factor = instance.bus_factor
    bus_factor.employee_count = EmployeeBusFactor.objects.filter(bus_factor=bus_factor).count()
    bus_factor.save()


# Сигнал для обновления employee_count при добавлении записи EmployeeKeyPeople
@receiver(post_save, sender=EmployeeKeyPeople)
def update_employee_count_on_save_key_people(sender, instance, created, **kwargs):
    if created:
        key_people = instance.key_people
        key_people.employee_count = EmployeeKeyPeople.objects.filter(key_people=key_people).count()
        key_people.save()

# Сигнал для обновления employee_count при удалении записи EmployeeKeyPeople
@receiver(post_delete, sender=EmployeeKeyPeople)
def update_employee_count_on_delete_key_people(sender, instance, **kwargs):
    key_people = instance.key_people
    key_people.employee_count = EmployeeKeyPeople.objects.filter(key_people=key_people).count()
    key_people.save()