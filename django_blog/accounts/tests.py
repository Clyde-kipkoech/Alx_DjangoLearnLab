from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AccountsTestCase(TestCase):
    def test_register_creates_user(self):
        resp = self.client.post(reverse('register'), {
            'username': 'tester',
            'email': 't@example.com',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(User.objects.filter(username='tester').exists())

    def test_profile_requires_login(self):
        resp = self.client.get(reverse('profile'))
        self.assertNotEqual(resp.status_code, 200)  # redirected to login
