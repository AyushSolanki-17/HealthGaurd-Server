from django.test import TestCase
from .models import HealthGuardUser
# Create your tests here.
import requests


class HealthGuardUserTestCase(TestCase):
    def test_CreateUsers(self):
        HealthGuardUser.objects.create_user(email='ayush17solanki@gmail.com', fname='Ayush', mobile='9825185887',
                                            password='Ayush123', gender='M', dob='2002-11-18')
        HealthGuardUser.objects.create_user(email='admin@hg.com', fname='Ayush', mobile='7016769052',
                                            password='admin123', gender='M', dob='2002-11-18')


    def check_users(self):
        obj = HealthGuardUser.objects.get(email='admin@hg.com')
        self.assertEqual(obj.mobile, '7016769052')
