from django.db.models.signals import post_save, post_delete
from django.db import transaction
from django.dispatch import receiver

from core.models import (
    EmployeeSkill,
    EmployeeCompetency,
    EmployeeBusFactor,
    EmployeeKeyPeople,
    EmployeeEngagement,
    PositionGrade,
    EmployeeTrainingApplication,
    EmployeeDevelopmentPlan,
    EmployeeKeyPeople,
)


@receiver(post_save, sender=EmployeeKeyPeople)
@receiver(post_delete, sender=EmployeeKeyPeople)
def update_employee_count(sender, instance, **kwargs):
    with transaction.atomic():
        key_people = instance.key_people
        key_people.employee_count = key_people.employees.count()
        key_people.save()


@receiver(post_save, sender=EmployeeDevelopmentPlan)
@receiver(post_delete, sender=EmployeeDevelopmentPlan)
def update_employee_count(sender, instance, **kwargs):
    with transaction.atomic():
        development_plan = instance.development_plan
        development_plan.employee_count = (
            development_plan.employeedevelopmentplan_set.count()
        )
        development_plan.save()


@receiver(post_save, sender=EmployeeTrainingApplication)
@receiver(post_delete, sender=EmployeeTrainingApplication)
def update_employee_count(sender, instance, **kwargs):
    with transaction.atomic():
        training_application = instance.training_application
        training_application.employee_count = (
            training_application.employeetrainingapplication_set.count()
        )
        training_application.save()


@receiver(post_save, sender=PositionGrade)
@receiver(post_delete, sender=PositionGrade)
def update_grade_count(sender, instance, **kwargs):
    with transaction.atomic():
        position = instance.position
        position.grade_count = position.position_grades.count()
        position.save()


@receiver(post_save, sender=EmployeeEngagement)
@receiver(post_delete, sender=EmployeeEngagement)
def update_employee_count(sender, instance, **kwargs):
    with transaction.atomic():
        engagement = instance.engagement
        engagement.employee_count = engagement.employee_engagements.count()
        engagement.save()


@receiver([post_save, post_delete], sender=EmployeeSkill)
def update_employee_count(sender, instance, **kwargs):
    with transaction.atomic():
        skill = instance.skill
        skill.employee_count = EmployeeSkill.objects.filter(
            skill=skill
        ).count()
        skill.save()


@receiver([post_save, post_delete], sender=EmployeeCompetency)
def update_employee_competency_count(sender, instance, **kwargs):
    with transaction.atomic():
        competency = instance.competency
        competency.employee_count = EmployeeCompetency.objects.filter(
            competency=competency
        ).count()
        competency.save()


@receiver(post_save, sender=EmployeeBusFactor)
def update_employee_count_on_save(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            bus_factor = instance.bus_factor
            bus_factor.employee_count = EmployeeBusFactor.objects.filter(
                bus_factor=bus_factor
            ).count()
            bus_factor.save()
