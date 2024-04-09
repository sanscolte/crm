from typing import Dict

from django.db.models import DecimalField
from django.test import TestCase

from crm.models import Service, Campaign, PotentialClient, Contract, ActiveClient


class TestServiceModel(TestCase):
    """Класс тестов модели услуг"""

    fixtures = [
        "03-services.json",
    ]

    def setUp(self):
        self.service = Service.objects.get(pk=7)

    def test_verbose_name(self):
        """Тестирование валидности имен полей модели"""

        field_verboses: Dict[str, str] = {
            "name": "название",
            "description": "описание",
            "cost": "стоимость",
        }
        for field_name, field_verbose in field_verboses.items():
            with self.subTest(field_name=field_name):
                self.assertEqual(self.service._meta.get_field(field_name).verbose_name, field_verbose)

    def test_name_max_length(self):
        """Тестирование максимальной длины поля name"""

        max_length: int | None = self.service._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)

    def test_cost_max_digits(self):
        """Тестирование максимального кол-ва цифр поля cost"""

        meta: DecimalField = self.service._meta.get_field("cost")
        max_digits, decimal_places = meta.max_digits, meta.decimal_places
        self.assertEqual(max_digits, 100)
        self.assertEqual(decimal_places, 2)


class TestCampaignModel(TestCase):
    """Класс тестов модели рекламной компании"""

    fixtures = [
        "03-services.json",
        "04-campaigns.json",
    ]

    def setUp(self):
        self.campaign = Campaign.objects.get(pk=1)

    def test_verbose_name(self):
        """Тестирование валидности имен полей модели"""

        field_verboses: Dict[str, str] = {
            "name": "название",
            "service": "услуга",
            "promotion_channel": "канал продвижения",
            "budget": "бюджет",
        }

        for field_name, field_verbose in field_verboses.items():
            with self.subTest(field_name=field_name):
                self.assertEqual(self.campaign._meta.get_field(field_name).verbose_name, field_verbose)

    def test_name_max_length(self):
        """Тестирование максимальной длины поля name"""

        max_length: int | None = self.campaign._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)

    def test_budget_max_digits(self):
        """Тестирование максимального кол-ва цифр поля cost"""

        meta: DecimalField = self.campaign._meta.get_field("budget")
        max_digits, decimal_places = meta.max_digits, meta.decimal_places
        self.assertEqual(max_digits, 10)
        self.assertEqual(decimal_places, 2)

    def test_promotion_channel_max_digits(self):
        """Тестирование максимального кол-ва цифр поля cost"""

        max_length: int | None = self.campaign._meta.get_field("promotion_channel").max_length
        self.assertEqual(max_length, 100)


class TestPotentialClientModel(TestCase):
    """Класс тестов модели потенциального клиента"""

    fixtures = [
        "03-services.json",
        "04-campaigns.json",
        "05-potential_clients.json",
    ]

    def setUp(self):
        self.potential_client = PotentialClient.objects.get(pk=1)

    def test_verbose_name(self):
        """Тестирование валидности имен полей модели"""

        field_verboses: Dict[str, str] = {
            "full_name": "Ф.И.О",
            "phone": "телефон",
            "email": "email",
            "campaign": "рекламная кампания",
        }
        for field_name, field_values in field_verboses.items():
            with self.subTest(filed_name=field_name):
                self.assertEqual(self.potential_client._meta.get_field(field_name).verbose_name, field_values)

    def test_full_name_max_length(self):
        """Тестирование максимальной длины поля full_name"""

        max_length: int | None = self.potential_client._meta.get_field("full_name").max_length
        self.assertEqual(max_length, 100)

    def test_phone_max_length(self):
        """Тестирование максимального кол-ва цифр поля телефона"""

        max_length: int | None = self.potential_client._meta.get_field("phone").max_length
        self.assertEqual(max_length, 11)


class TestContractModel(TestCase):
    fixtures = [
        "03-services.json",
        "06-contracts.json",
    ]

    def setUp(self):
        self.contract = Contract.objects.get(pk=1)

    def test_verbose_name(self):
        """Тестирование валидности имени поля модели"""
        field_verboses: Dict[str, str] = {
            "name": "название",
            "service": "услуга",
            "document": "документ",
            "conclusion_date": "дата заключения",
        }
        for field_name, field_values in field_verboses.items():
            with self.subTest(filed_name=field_name):
                self.assertEqual(self.contract._meta.get_field(field_name).verbose_name, field_values)

    def test_name_max_length(self):
        """Тестирование максимальной длины поля name"""

        max_length: int | None = self.contract._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)

    def test_amount_max_digits(self):
        """Тестирование максимального кол-ва цифр поля amount"""

        meta: DecimalField = self.contract._meta.get_field("amount")
        max_digits, decimal_places = meta.max_digits, meta.decimal_places
        self.assertEqual(max_digits, 10)
        self.assertEqual(decimal_places, 2)


class TestActiveClientModel(TestCase):
    fixtures = [
        "03-services.json",
        "04-campaigns.json",
        "05-potential_clients.json",
        "06-contracts.json",
        "07-active_clients.json",
    ]

    def setUp(self):
        self.active_client = ActiveClient.objects.get(pk=1)

    def test_verbose_name(self):
        """Тестирование валидности имен полей модели"""

        field_verboses: Dict[str, str] = {
            "potential_client": "потенциальный клиент",
            "contract": "контракт",
        }

        for field_name, field_values in field_verboses.items():
            with self.subTest(filed_name=field_name):
                self.assertEqual(self.active_client._meta.get_field(field_name).verbose_name, field_values)
