from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
import uuid



class Employee(AbstractUser):
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

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"

