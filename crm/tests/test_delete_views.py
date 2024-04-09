from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy


class TestDeleteViews(TestCase):
    """Класс тестов для представлений удаления экземпляров"""

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

    def test_delete_service_by_admin(self):
        """Тест для удаления услуги под аккаунтом админа"""

        self.client.force_login(self.admin)
        service_pk: int = 7

        response = self.client.delete(reverse_lazy("crm:service_delete", kwargs={"pk": service_pk}))
        self.assertEqual(response.status_code, 302)

    def test_delete_service_by_not_admin(self):
        """Тест удаления услуги под невалидным аккаунтом"""
        self.client.force_login(self.operator)
        service_pk: int = 7

        response = self.client.delete(reverse_lazy("crm:service_delete", kwargs={"pk": service_pk}))

        with self.assertRaises(AssertionError):
            self.assertEqual(response.status_code, 302)

    def test_delete_campaign_by_admin(self):
        """Тест для удаления рекламной компании под аккаунтом админа"""

        self.client.force_login(self.admin)
        campaign_pk: int = 1

        response = self.client.delete(reverse_lazy("crm:campaign_delete", kwargs={"pk": campaign_pk}))
        self.assertEqual(response.status_code, 302)

    def test_delete_campaign_by_not_admin(self):
        """Тест удаления рекламной компании под невалидным аккаунтом"""
        self.client.force_login(self.operator)
        campaign_pk: int = 1

        response = self.client.delete(reverse_lazy("crm:campaign_delete", kwargs={"pk": campaign_pk}))

        with self.assertRaises(AssertionError):
            self.assertEqual(response.status_code, 302)

    def test_delete_potential_client_by_admin(self):
        """Тест для удаления потенциального клиента под аккаунтом админа"""

        self.client.force_login(self.admin)
        potential_client_pk: int = 1

        response = self.client.delete(reverse_lazy("crm:potential_client_delete", kwargs={"pk": potential_client_pk}))
        self.assertEqual(response.status_code, 302)

    def test_delete_potential_client_by_not_admin(self):
        """Тест удаления потенциального клиента под невалидным аккаунтом"""
        self.client.force_login(self.operator)
        potential_client_pk: int = 1

        response = self.client.delete(reverse_lazy("crm:potential_client_delete", kwargs={"pk": potential_client_pk}))

        with self.assertRaises(AssertionError):
            self.assertEqual(response.status_code, 302)

    def test_delete_contract_by_admin(self):
        """Тест для удаления контракта под аккаунтом админа"""

        self.client.force_login(self.admin)
        potential_client_pk: int = 1

        response = self.client.delete(reverse_lazy("crm:contract_delete", kwargs={"pk": potential_client_pk}))
        self.assertEqual(response.status_code, 302)

    def test_delete_contract_by_not_admin(self):
        """Тест удаления контракта под невалидным аккаунтом"""
        self.client.force_login(self.operator)
        potential_client_pk: int = 1

        response = self.client.delete(reverse_lazy("crm:contract_delete", kwargs={"pk": potential_client_pk}))

        with self.assertRaises(AssertionError):
            self.assertEqual(response.status_code, 302)

    def test_delete_active_client_by_admin(self):
        """Тест для удаления активного клиента под аккаунтом админа"""

        self.client.force_login(self.admin)
        potential_client_pk: int = 1

        response = self.client.delete(reverse_lazy("crm:active_client_delete", kwargs={"pk": potential_client_pk}))
        self.assertEqual(response.status_code, 302)

    def test_delete_active_client_by_not_admin(self):
        """Тест удаления активного клиента под невалидным аккаунтом"""
        self.client.force_login(self.operator)
        potential_client_pk: int = 1

        response = self.client.delete(reverse_lazy("crm:active_client_delete", kwargs={"pk": potential_client_pk}))

        with self.assertRaises(AssertionError):
            self.assertEqual(response.status_code, 302)
