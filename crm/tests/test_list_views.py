from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy

from crm.models import PotentialClient


class TestListViews(TestCase):
    """Класс тестов для представлений списка экземпляров модели"""

    fixtures = [
        "01-groups.json",
        "02-users.json",
        "03-services.json",
        "04-campaigns.json",
        "05-potential_clients.json",
        "06-contracts.json",
        "07-active_clients.json",
    ]

    @classmethod
    def setUpClass(cls):
        """Объявление подготовленных юзеров с группами прав"""

        super().setUpClass()
        cls.admin = User.objects.get(username="admin")
        cls.operator = User.objects.get(username="operator")
        cls.marketer = User.objects.get(username="marketer")
        cls.manager = User.objects.get(username="manager")

    def test_list_service_by_marketer(self):
        """Тест получения списка услуг под аккаунтом маркетолога"""

        self.client.force_login(self.marketer)

        response = self.client.get(reverse_lazy("crm:services"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New service")

    def test_list_service_by_not_marketer(self):
        """Тест получения списка услуг под невалидным аккаунтом"""

        self.client.force_login(self.operator)

        response = self.client.get(reverse_lazy("crm:services"))

        with self.assertRaises(AssertionError):
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "New service")

    def test_list_campaign_by_marketer(self):
        """Тест получения списка рекламных компаний под аккаунтом маркетолога"""

        self.client.force_login(self.marketer)

        response = self.client.get(reverse_lazy("crm:campaigns"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New campaign")

    def test_list_campaign_by_not_marketer(self):
        """Тест получения списка рекламных компаний под невалидным аккаунтом"""

        self.client.force_login(self.operator)

        response = self.client.get(reverse_lazy("crm:campaigns"))

        with self.assertRaises(AssertionError):
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "New advirtising campaign")

    def test_list_potential_client_by_manager(self):
        """Тест получения списка потенциальных клиентов под аккаунтом менеджера"""

        self.client.force_login(self.manager)

        response = self.client.get(reverse_lazy("crm:potential_clients"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New potential client")

    def test_list_potential_client_by_not_marketer(self):
        """Тест получения списка потенциальных клиентов под невалидным аккаунтом"""

        self.client.force_login(self.marketer)

        response = self.client.get(reverse_lazy("crm:potential_clients"))

        with self.assertRaises(AssertionError):
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "New potential client")

    def test_list_contract_by_manager(self):
        """Тест получения списка контрактов под аккаунтом менеджера"""

        self.client.force_login(self.manager)

        response = self.client.get(reverse_lazy("crm:contracts"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New contract")

    def test_list_contract_by_not_manager(self):
        """Тест получения списка контрактов под невалидным аккаунтом"""

        self.client.force_login(self.operator)

        response = self.client.get(reverse_lazy("crm:contracts"))

        with self.assertRaises(AssertionError):
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "New contract")

    def test_list_active_client_by_admin(self):
        """Тест получения списка активных клиентов под аккаунтом админа"""

        self.client.force_login(self.admin)
        potential_client_pk = PotentialClient.objects.get(pk=1).pk

        response = self.client.get(reverse_lazy("crm:active_clients"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, potential_client_pk)

    def test_list_active_client_by_not_admin(self):
        """Тест получения списка активных клиентов под невалидным аккаунтом"""

        self.client.force_login(self.operator)
        potential_client_pk = PotentialClient.objects.get(pk=1).pk

        response = self.client.get(reverse_lazy("crm:active_clients"))

        with self.assertRaises(AssertionError):
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, potential_client_pk)
