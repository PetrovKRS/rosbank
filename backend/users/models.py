from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """ Модель пользователя. """

    email = models.EmailField(
        max_length=150,
        unique=True,
        verbose_name='E-mail',
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=(
            validate_me,
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='В имени пользователя можно использовать'
                        ' только буквы, цифры и символы "@/./+/-/_"!',
            ),
        ),
        verbose_name='Имя пользователя',
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
    )
    password = models.CharField(
        max_length=21,
        verbose_name='Пароль',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = (
            'username',
        )

    def __str__(self):
        return self.username
