from rest_framework import status, viewsets, mixins
from rest_framework.permissions import AllowAny

from core.models import Employee
from .serializers import EmployeeSerializer

class EmployeeViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
