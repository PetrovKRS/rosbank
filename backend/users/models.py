from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
import uuid


class ManagerTeam(AbstractUser):
    """ Модель менеджера. """

    username = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Логин'
    )
    email = models.EmailField(
        max_length=100,
        unique=True,
        verbose_name='E-mail'
    )
    password = models.CharField(
        max_length=100,
        verbose_name='Пароль',
        validators=(
            RegexValidator(
                regex=r'^.{4,}$',
                message='Пароль должен быть не менее 4-х символов'
            ),
        )
    )

    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'
        constraints = (
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_username_email'
            ),
        )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.pk})"
