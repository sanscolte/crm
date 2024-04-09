from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy

from crm.models import Contract


class TestDetailViews(TestCase):
    """Класс тестов для представлений деталей экземпляров"""

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

    def test_details_service_by_marketer(self):
        """Тест получения деталей услуги под аккаунтом маркетолога"""

        self.client.force_login(self.marketer)
        service_pk: int = 7

        response = self.client.get(reverse_lazy("crm:service_details", kwargs={"pk": service_pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is a same new service")

    def test_details_service_by_not_marketer(self):
        """Тест получения деталей услуги под невалидным аккаунтом"""

        self.client.force_login(self.operator)
        service_pk: int = 7

        response = self.client.get(reverse_lazy("crm:service_details", kwargs={"pk": service_pk}))

        with self.assertRaises(AssertionError):
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "This is a same new service")

    def test_details_campaign_by_marketer(self):
        """Тест получения деталей рекламной компании под аккаунтом маркетолога"""

        self.client.force_login(self.marketer)
        campaign_pk: int = 1

        response = self.client.get(reverse_lazy("crm:campaign_details", kwargs={"pk": campaign_pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New promotion channel")

    def test_details_campaign_by_not_marketer(self):
        """Тест получения деталей рекламной компании под невалидным аккаунтом"""

        self.client.force_login(self.operator)
        campaign_pk: int = 1

        response = self.client.get(reverse_lazy("crm:campaign_details", kwargs={"pk": campaign_pk}))

        with self.assertRaises(AssertionError):
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "New promotion channel")

    def test_details_potential_client_by_operator(self):
        """Тест получения деталей потенциального клиента под аккаунтом оператора"""

        self.client.force_login(self.operator)
        potential_client_pk: int = 1

        response = self.client.get(reverse_lazy("crm:potential_client_details", kwargs={"pk": potential_client_pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "potentialclient@gmail.com")

    def test_details_potential_client_by_not_operator(self):
        """Тест получения деталей потенциального клиента под невалидным аккаунтом"""

        self.client.force_login(self.marketer)
        potential_client_pk: int = 1

        response = self.client.get(reverse_lazy("crm:potential_client_details", kwargs={"pk": potential_client_pk}))

        with self.assertRaises(AssertionError):
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "potentialclient@gmail.com")

    def test_details_contract_by_manager(self):
        """Тест получения деталей контракта под аккаунтом менеджера"""

        self.client.force_login(self.manager)
        potential_client_pk: int = 1

        response = self.client.get(reverse_lazy("crm:contract_details", kwargs={"pk": potential_client_pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "documents/manage.py")

    def test_details_contract_by_not_manager(self):
        """Тест получения деталей контракта под невалидным аккаунтом"""

        self.client.force_login(self.operator)
        potential_client_pk: int = 1

        response = self.client.get(reverse_lazy("crm:contract_details", kwargs={"pk": potential_client_pk}))

        with self.assertRaises(AssertionError):
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "documents/manage.py")

    def test_details_active_client_by_admin(self):
        """Тест получения деталей активного клиента под аккаунтом админ"""

        self.client.force_login(self.admin)
        contract = Contract.objects.get(pk=1)
        potential_client_pk: int = 1

        response = self.client.get(reverse_lazy("crm:active_client_details", kwargs={"pk": potential_client_pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, contract.name)

    def test_details_active_client_by_not_admin(self):
        """Тест получения деталей активного клиента под невалидным аккаунтом"""

        self.client.force_login(self.operator)
        contract = Contract.objects.get(pk=1)
        potential_client_pk: int = 1

        response = self.client.get(reverse_lazy("crm:active_client_details", kwargs={"pk": potential_client_pk}))

        with self.assertRaises(AssertionError):
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, contract.name)
