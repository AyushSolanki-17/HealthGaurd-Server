import uuid
from django.db import models
from MainWebApp.models import HealthGuardUser, HealthGuardDoctor
import datetime
import json


class TestReportManager(models.Manager):

    def new_test_report(self, user_email, t_type, symptoms, result, chances, date):
        user = HealthGuardUser.objects.get(email=user_email)
        symptoms = json.loads(symptoms)
        symptoms_list = ""
        for symp in symptoms:
            if symptoms[symp] > 0 and symp != 'days':
                symptoms_list += symp + ", "
        symptoms_list = symptoms_list[:-2]
        report = self.model(
            user=user,
            type=t_type,
            symptoms=symptoms_list,
            result=result,
            chances=chances,
            days=symptoms['days'],
            date=date
        )
        report.save(using=self._db)
        return report


class TestReport(models.Model):
    Test_Type_Choices = [
        ("general", "General"),
        ("dengue", "Dengue"),
        ("chikungunya", "Chikungunya"),
        ("malaria", "Malaria"),
        ("covid", "Covid")
    ]
    test_id = models.UUIDField(
        verbose_name='test ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        HealthGuardUser,
        on_delete=models.CASCADE,
        verbose_name='user'
    )
    type = models.CharField(
        max_length=55,
        verbose_name='test type',
        choices=Test_Type_Choices,
    )
    symptoms = models.CharField(
        max_length=500,
        verbose_name='symptoms'
    )
    result = models.CharField(
        max_length=300,
        verbose_name='result',
    )
    days = models.IntegerField(
        verbose_name='days'
    )
    chances = models.IntegerField(
        verbose_name='chances'
    )
    is_open_for_verification = models.BooleanField(
        default=False,
        verbose_name='is_open_for_verification'
    )
    date = models.DateField(
        verbose_name='Date of Test',
        default=datetime.date.today
    )
    doctor = models.ForeignKey(
        HealthGuardDoctor,
        blank=True,
        null=True,
        verbose_name='verifier doctor',
        on_delete=models.SET_NULL
    )
    doctor_description = models.CharField(
        verbose_name='description by doctor',
        blank=True,
        default='',
        null=True,
        max_length=1000
    )

    objects = TestReportManager()

    def __str__(self):
        return self.type + ' : ' + self.user.email + " : " + self.result

    class Meta:
        db_table = 'TestReports'

