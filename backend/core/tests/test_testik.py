from django.urls import reverse, get_resolver
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import (
    Employee,
    EmployeeTeam,
    Team,
    ManagerTeam,
)

from core.tests.factories import (
    EmployeeFactory,
    TeamFactory,
    ManagerTeamFactory,
)


class UrlTests(APITestCase):

    def setUp(self):

        self.manager = ManagerTeamFactory()

        self.team = TeamFactory()

        self.employee = EmployeeFactory()

        self.employee_team = EmployeeTeam.objects.create(
            manager=self.manager, team=self.team
        )
        self.employee_team.employee.add(self.employee)

    def test_metric_development_plan(self):
        url = reverse(
            'metric-list',
            kwargs={'metric_type': 'development_plan', 'employee_id': 1},
        )
        data = {
            "startPeriod": {"month": "August", "year": "2024"},
            "endPeriod": {"month": "October", "year": "2024"},
        }
        response = self.client.post(url, data=data, format='json')

        # Проверяем, что статус ответа 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем наличие ключей в ответе
        response_data = response.json()
        self.assertIn('dashboard', response_data)
        self.assertIn('completionForToday', response_data)

    def test_metric_involvement(self):
        url = reverse(
            'metric-list',
            kwargs={'metric_type': 'involvement', 'employee_id': 1},
        )
        data = {
            "startPeriod": {"month": "August", "year": "2024"},
            "endPeriod": {"month": "October", "year": "2024"},
        }
        response = self.client.post(url, data=data, format='json')

        # Проверяем статус
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем наличие ключей
        response_data = response.json()
        self.assertIn('dashboard', response_data)
        self.assertIn('completionForToday', response_data)

    # ==================================================================================================================

    def test_team_count_employees(self):
        # Укажите полный путь
        url = reverse(
            'count_employees-list', kwargs={'team_slug': self.team.slug}
        )  # замените на правильный путь вашего API

        # Вывод отладочной информации
        print("Тестируемый URL:", url)

        response = self.client.post(
            url,
            {
                "startPeriod": {"month": "August", "year": 2024},
                "endPeriod": {"month": "October", "year": 2024},
            },
            format='json',
        )  # указываем формат как json

        # Вывод отладочной информации
        print("Статус код ответа:", response.status_code)
        print(
            "Ответ от сервера:", response.data
        )  # Если у вас есть сообщение об ошибке

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_individual_competencies(self):
        url = reverse(
            'individual_competencies-list',
            kwargs={'team_slug': self.team.slug},
        )
        data = {"skillDomen": "hard"}
        response = self.client.post(url, data=data, format='json')

        # Проверяем статус
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем наличие ключей
        response_data = response.json()
        self.assertIn('data', response_data)

    def test_competency_level(self):
        url = reverse(
            'competency_level-list', kwargs={'team_slug': self.team.slug}
        )
        data = {"skillDomen": "hard", "competencyId": 1}
        response = self.client.post(url, data=data, format='json')

        # Проверяем статус
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем наличие ключей
        response_data = response.json()
        self.assertIn('data', response_data)
