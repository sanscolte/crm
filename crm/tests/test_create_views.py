from typing import Dict, Union

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.test import TestCase
from django.urls import reverse_lazy

from crm.models import (
    Service,
    Campaign,
    PotentialClient,
    Contract,
    ActiveClient,
)


class TestCreateViews(TestCase):
    """Класс тестов для представлений создания экземпляров"""

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

    def test_create_service_by_marketer(self):
        """Тест создания услуги под аккаунтом маркетолога"""

        self.client.force_login(self.marketer)
        data: Dict[str, Union[str, float]] = {
            "name": "Test Service",
            "description": "Test Description",
            "cost": 100.00,
        }
        response = self.client.post(reverse_lazy("crm:create_service"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Service.objects.filter(name="Test Service").exists())

    def test_create_service_by_not_marketer(self):
        """Тест создания услуги под невалидным аккаунтом"""

        self.client.force_login(self.operator)
        data: Dict[str, Union[str, float]] = {
            "name": "Test Service",
            "description": "Test Description",
            "cost": 100.00,
        }
        response = self.client.post(reverse_lazy("crm:create_service"), data=data)

        with self.assertRaises(AssertionError):
            self.assertEqual(response.status_code, 302)
            self.assertTrue(Service.objects.filter(name="Test Service").exists())

    def test_create_campaign_by_marketer(self):
        """Тест создания рекламной компании под аккаунтом маркетолога"""

        self.client.force_login(self.marketer)
        service = Service.objects.get(pk=7)
        data: Dict[str, Union[str, float, int]] = {
            "name": "Test Campaign",
            "service": service.pk,
            "promotion_channel": "Test Promotion Channel",
            "budget": 1000.00,
        }
        response = self.client.post(reverse_lazy("crm:create_campaign"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Campaign.objects.filter(name="Test Campaign").exists())

    def test_create_campaign_by_not_marketer(self):
        """Тест создания рекламной компании под невалидным аккаунтом"""

        self.client.force_login(self.operator)
        service = Service.objects.get(pk=7)
        data: Dict[str, Union[str, float, int]] = {
            "name": "Test Campaign",
            "service": service.pk,
            "promotion_channel": "Test Promotion Channel",
            "budget": 1000.00,
        }
        response = self.client.post(reverse_lazy("crm:create_campaign"), data=data)

        with self.assertRaises(AssertionError):
            self.assertEqual(response.status_code, 302)
            self.assertTrue(Campaign.objects.filter(name="Test Campaign").exists())

    def test_create_potential_client_by_operator(self):
        """Тест создания потенциального клиента под аккаунтом оператора"""

        self.client.force_login(self.operator)
        campaign = Campaign.objects.get(pk=1)
        data: Dict[str, Union[str, int]] = {
            "full_name": "Test Potential Client",
            "phone": "+1234567890",
            "email": "testpotentialclient@example.com",
            "campaign": campaign.pk,
        }
        response = self.client.post(reverse_lazy("crm:create_potential_client"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(PotentialClient.objects.filter(full_name="Test Potential Client").exists())

    def test_create_potential_client_by_not_operator(self):
        """Тест создания потенциального клиента под невалидным аккаунтом"""

        self.client.force_login(self.marketer)
        campaign = Campaign.objects.get(pk=1)
        data: Dict[str, Union[str, int]] = {
            "full_name": "Test Potential Client",
            "phone": "+1234567890",
            "email": "testpotentialclient@example.com",
            "campaign": campaign.pk,
        }
        response = self.client.post(reverse_lazy("crm:create_potential_client"), data=data)

        with self.assertRaises(AssertionError):
            self.assertEqual(response.status_code, 302)
            self.assertTrue(PotentialClient.objects.filter(full_name="Test Potential Client").exists())

    def test_create_contract_by_manager(self):
        """Тест создания контракта под аккаунтом менеджера"""

        self.client.force_login(self.manager)
        service = Service.objects.get(pk=7)

        with open("./uploads/documents/test.json", "r", encoding="utf-8") as f:
            file_content: str = f.read()

        file: ContentFile = ContentFile(file_content, name="test.json")

        data: Dict[str, Union[str, float, int, ContentFile]] = {
            "name": "Test Contract",
            "service": service.pk,
            "document": file,
            "conclusion_date": "2020-01-01",
            "validity_period": 120,
            "amount": 1000.02,
        }

        response = self.client.post(reverse_lazy("crm:create_contract"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Contract.objects.filter(name="Test Contract").exists())

    def test_create_contract_by_not_manager(self):
        """Тест создания контракта под невалидным аккаунтом"""

        self.client.force_login(self.operator)
        service = Service.objects.get(pk=7)

        with open("./uploads/documents/test.json", "r", encoding="utf-8") as f:
            file_content: str = f.read()

        file: ContentFile = ContentFile(file_content, name="test.json")

        data: Dict[str, Union[str, float, int, ContentFile]] = {
            "name": "Test Contract",
            "service": service.pk,
            "document": file,
            "conclusion_date": "2020-01-01",
            "validity_period": 120,
            "amount": 1000.02,
        }

        response = self.client.post(reverse_lazy("crm:create_contract"), data=data)

        with self.assertRaises(AssertionError):
            self.assertEqual(response.status_code, 302)
            self.assertTrue(Contract.objects.filter(name="Test Contract").exists())

    def test_create_active_client_by_manager(self):
        """Тест создания активного клиента под аккаунтом менеджера"""

        self.client.force_login(self.manager)
        potential_client = PotentialClient.objects.get(pk=6)
        contract = Contract.objects.get(pk=6)

        data: Dict[str, Union[str, int]] = {
            "contract": contract.pk,
        }

        response = self.client.post(
            reverse_lazy("crm:create_active_client", kwargs={"pk": potential_client.pk}),
            data=data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ActiveClient.objects.filter(potential_client=potential_client.pk).exists())

    def test_create_active_client_by_not_manager(self):
        """Тест создания активного клиента под невалидным аккаунтом"""

        self.client.force_login(self.operator)
        potential_client = PotentialClient.objects.get(pk=6)
        contract = Contract.objects.get(pk=6)

        data: Dict[str, int] = {
            "potential_client": potential_client.pk,
            "contract": contract.pk,
        }

        response = self.client.post(
            reverse_lazy("crm:create_active_client", kwargs={"pk": potential_client.pk}), data=data
        )

        with self.assertRaises(AssertionError):
            self.assertEqual(response.status_code, 302)
            self.assertTrue(ActiveClient.objects.filter(potential_client=potential_client.pk).exists())
