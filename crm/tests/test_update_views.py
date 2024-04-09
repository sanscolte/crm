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


class TestUpdateViews(TestCase):
    """Класс тестов для представлений обновления экземпляров модели"""

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

    def test_update_service_by_marketer(self):
        """Тест обновления услуги под аккаунтом админа"""

        self.client.force_login(self.marketer)
        service_pk: int = 7
        updated_data: Dict[str, Union[str, float]] = {
            "name": "A NEW NAME",
            "description": "Test Descriptionn",
            "cost": 200.00,
        }
        response = self.client.post(
            reverse_lazy("crm:service_update", kwargs={"pk": service_pk}),
            data=updated_data,
        )
        service = Service.objects.get(pk=service_pk)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(service.name, "A NEW NAME")

    def test_update_service_by_not_marketer(self):
        """Тест обновления услуги под невалидным аккаунтом"""

        self.client.force_login(self.operator)
        service_pk: int = 7
        updated_data: Dict[str, Union[str, float]] = {
            "name": "A NEW NAME",
            "description": "Test Descriptionn",
            "cost": 200.00,
        }
        response = self.client.post(
            reverse_lazy("crm:service_update", kwargs={"pk": service_pk}),
            data=updated_data,
        )
        service = Service.objects.get(pk=service_pk)

        with self.assertRaises(AssertionError):
            self.assertEqual(response.status_code, 302)
            self.assertEqual(service.name, "A NEW NAME")

    def test_update_campaign_by_marketer(self):
        """Тест обновления рекламной компании под аккаунтом админа"""

        self.client.force_login(self.marketer)
        service = Service.objects.get(pk=7)
        campaign_pk: int = 1
        updated_data: Dict[str, Union[str, float, int]] = {
            "name": "NEW TEST CAMPAIGN",
            "service": service.pk,
            "promotion_channel": "New promotion channel",
            "budget": 750.01,
        }

        response = self.client.post(
            reverse_lazy("crm:campaign_update", kwargs={"pk": campaign_pk}),
            data=updated_data,
        )
        campaign = Campaign.objects.get(pk=campaign_pk)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(campaign.name, "NEW TEST CAMPAIGN")

    def test_update_campaign_by_not_marketer(self):
        """Тест обновления рекламной компании под невалидным аккаунтом"""

        self.client.force_login(self.operator)
        service = Service.objects.get(pk=7)
        campaign_pk: int = 1
        updated_data: Dict[str, Union[str, float, int]] = {
            "name": "NEW TEST CAMPAIGN",
            "service": service.pk,
            "promotion_channel": "New promotion channel",
            "budget": 750.01,
        }

        response = self.client.post(
            reverse_lazy("crm:campaign_update", kwargs={"pk": campaign_pk}),
            data=updated_data,
        )
        campaign = Campaign.objects.get(pk=campaign_pk)

        with self.assertRaises(AssertionError):
            self.assertEqual(response.status_code, 302)
            self.assertEqual(campaign.name, "NEW TEST CAMPAIGN")

    def test_update_potential_client_by_operator(self):
        """Тест обновления потенциального клиента под аккаунтом админа"""

        self.client.force_login(self.operator)
        potential_client_pk: int = 1
        campaign = Campaign.objects.get(pk=1)

        updated_data: Dict[str, Union[str, int]] = {
            "full_name": "NEW POTENTIAL CLIENT",
            "phone": "+1234567890",
            "email": "testpotentialclient@example.com",
            "campaign": campaign.pk,
        }
        response = self.client.post(
            reverse_lazy("crm:potential_client_update", kwargs={"pk": potential_client_pk}),
            data=updated_data,
        )
        potential_client = PotentialClient.objects.get(pk=potential_client_pk)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(potential_client.full_name, "NEW POTENTIAL CLIENT")

    def test_update_potential_client_by_not_operator(self):
        """Тест обновления потенциального клиента под невалидным аккаунтом"""

        self.client.force_login(self.marketer)
        potential_client_pk: int = 1
        campaign = Campaign.objects.get(pk=1)

        updated_data: Dict[str, Union[str, int]] = {
            "full_name": "NEW POTENTIAL CLIENT",
            "phone": "+1234567890",
            "email": "testpotentialclient@example.com",
            "campaign": campaign.pk,
        }
        response = self.client.post(
            reverse_lazy("crm:potential_client_update", kwargs={"pk": potential_client_pk}),
            data=updated_data,
        )
        potential_client = PotentialClient.objects.get(pk=potential_client_pk)

        with self.assertRaises(AssertionError):
            self.assertEqual(response.status_code, 302)
            self.assertEqual(potential_client.full_name, "NEW POTENTIAL CLIENT")

    def test_update_contract_by_manager(self):
        """Тест обновления контракта под аккаунтом админа"""

        self.client.force_login(self.manager)
        contract_pk: int = 1
        service = Service.objects.get(pk=7)

        with open("./uploads/documents/test.json", "r", encoding="utf-8") as f:
            file_content: str = f.read()

        file: ContentFile = ContentFile(file_content, name="test.json")

        updated_data: Dict[str, Union[str, float, int, ContentFile]] = {
            "name": "NEW CONTRACT",
            "service": service.pk,
            "document": file,
            "conclusion_date": "2020-01-01",
            "validity_period": 120,
            "amount": 1000.02,
        }
        response = self.client.post(
            reverse_lazy("crm:contract_update", kwargs={"pk": contract_pk}),
            data=updated_data,
        )
        contract = Contract.objects.get(pk=contract_pk)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(contract.name, "NEW CONTRACT")

    def test_update_contract_by_not_manager(self):
        """Тест обновления контракта под невалидным аккаунтом"""

        self.client.force_login(self.operator)
        contract_pk: int = 1
        service = Service.objects.get(pk=7)

        with open("./uploads/documents/test.json", "r", encoding="utf-8") as f:
            file_content: str = f.read()

        file: ContentFile = ContentFile(file_content, name="test.json")

        updated_data: Dict[str, Union[str, float, int, ContentFile]] = {
            "name": "NEW CONTRACT",
            "service": service.pk,
            "document": file,
            "conclusion_date": "2020-01-01",
            "validity_period": 120,
            "amount": 1000.02,
        }
        response = self.client.post(
            reverse_lazy("crm:contract_update", kwargs={"pk": contract_pk}),
            data=updated_data,
        )
        contract = Contract.objects.get(pk=contract_pk)

        with self.assertRaises(AssertionError):
            self.assertEqual(response.status_code, 302)
            self.assertEqual(contract.name, "NEW CONTRACT")

    def test_update_active_client_by_admin(self):
        """Тест обновления активного клиента под аккаунтом админа"""

        self.client.force_login(self.admin)
        active_client_pk: int = 1
        potential_client = PotentialClient.objects.get(pk=1)
        contract = Contract.objects.get(pk=7)

        updated_data: Dict[str, Union[str, float, int]] = {
            "potential_client": potential_client.pk,
            "contract": contract.pk,
        }

        response = self.client.post(
            reverse_lazy("crm:active_client_update", kwargs={"pk": potential_client.pk}),
            data=updated_data,
        )
        active_client = ActiveClient.objects.get(pk=active_client_pk)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(active_client.contract.pk, contract.pk)

    def test_update_active_client_by_not_admin(self):
        """Тест обновления активного клиента под невалидным аккаунтом"""

        self.client.force_login(self.operator)
        active_client_pk: int = 1
        potential_client = PotentialClient.objects.get(pk=1)
        contract = Contract.objects.get(pk=7)

        updated_data: Dict[str, Union[str, float, int]] = {
            "potential_client": potential_client.pk,
            "contract": contract.pk,
        }

        response = self.client.post(
            reverse_lazy("crm:active_client_update", kwargs={"pk": potential_client.pk}), data=updated_data
        )
        active_client = ActiveClient.objects.get(pk=active_client_pk)

        with self.assertRaises(AssertionError):
            self.assertEqual(response.status_code, 302)
            self.assertEqual(active_client.contract.pk, contract.pk)
