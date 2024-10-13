from rest_framework import serializers
from django.test import TestCase
from core.models import Employee, Team, ManagerTeam, EmployeeTeam
from api.serializers import EmployeeSerializer, SkillSerializer
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


