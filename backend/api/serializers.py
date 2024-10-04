from rest_framework import serializers

from core.models import (
    Employee,
)

class EmployeeSerializer(serializers.ModelSerializer):
    """ Employee Serializer. """

    # speciality =

    class Meta:
        model = Employee
        fields = (
            'id', 'speciality',
        )