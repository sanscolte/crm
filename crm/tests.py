from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.urls import reverse_lazy

from crm.models import Service


class TestViews(TestCase):
    fixtures = [
        'fixtures/users.json',
    ]

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.get(username='marketer')

    def setUp(self):
        self.client.force_login(self.user)

    def test_create_service(self):
        data = {
            'name': 'Test Service',
            'description': 'Test Description',
            'cost': 100.00,
        }
        response = self.client.post(reverse_lazy('crm:create_service'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Service.objects.filter(name='Test Service').exists())
