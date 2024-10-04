from django.core.exceptions import ValidationError


def validate_me(username):
    if username == 'me':
        raise ValidationError(
            'Использовать имя me запрещено!'
        )
