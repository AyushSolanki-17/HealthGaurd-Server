from django.test import TestCase
from .models import TestReport
from MainWebApp.models import HealthGuardUser
# Create your tests here.
import datetime


class DiseaseTestCase(TestCase):
    def test_start(self):
        HealthGuardUser.objects.create_user(email='ayush17solanki@gmail.com', fname='Ayush', mobile='9825185887',
                                            password='Ayush123', gender='M', dob='2002-11-18')


def testreports():
    '''from DiseasePrediction.tests import testreports'''
    report = TestReport.objects.new_test_report(
        user_email='ayush17solanki@gmail.com',
        t_type='dengue',
        symptoms={
            'fever': 2,
            'headache': 0,
            'vom': 1,
        },
        result='Dengue Positive',
        description='You have tested positive for dengue',
        date=datetime.date.today(),
    )
    print(report)

