from datetime import datetime
from django.db import models
from MainWebApp.models import HealthGuardDoctor, HealthGuardUser
import uuid
from django.db.models.signals import post_save
# Create your models here.


class Clinic(models.Model):
    clinic_id = models.AutoField(
        primary_key=True
    )
    doctor = models.ForeignKey(HealthGuardDoctor,
                               on_delete=models.CASCADE,
                               verbose_name="Clinic Doctor"
                               )
    address = models.TextField(
        max_length=500,
        verbose_name="Clinic address",
    )
    city = models.TextField(
        max_length=100,
        verbose_name="Clinic City"
    )

    class Meta:
        db_table = 'Clinics'


class UserAppointmentPoint(models.Model):
    user = models.OneToOneField(HealthGuardUser,
                                models.CASCADE,
                                verbose_name="user"
                                )
    appointment_points = models.IntegerField(
        default=2,
        verbose_name="Appointment points"
    )

    class Meta:
        db_table = 'UserAppointmentPoints'


class AppointmentManager(models.Manager):
    def appointment_request(self,user_email, clinicId, dt):
        user = HealthGuardUser.objects.get(email=user_email)
        points = UserAppointmentPoint.objects.get(user=user)
        if points.appointment_points>0:
            points.appointment_points -= 1
            points.save()
            clinic = Clinic.objects.get(clinic_id=clinicId)
            dts = str(dt).split("-")
            dt = datetime(int(dts[0]), int(dts[1]), int(dts[2]), int(dts[3]), int(dts[4]))
            appointment = self.model(user=user, clinic=clinic, appointment_date_time=dt)
            appointment.save()
            return appointment.appointment_status
        else:
            return "Maximum limit of request appointments reached"


class Appointment(models.Model):
    appointment_id = models.UUIDField(
        verbose_name="Appointment ID",
        editable=False,
        primary_key=True,
        default=uuid.uuid4
    )
    clinic = models.ForeignKey(
        Clinic,
        on_delete=models.CASCADE,
        verbose_name="Clinic",
    )
    user = models.ForeignKey(
        HealthGuardUser,
        on_delete=models.CASCADE,
        verbose_name="User",
    )
    appointment_date_time = models.DateTimeField(
        verbose_name="Appointment DateTime"
    )
    appointment_status = models.TextField(
        verbose_name="Current Status",
        default="pending"
    )
    appointment_approval = models.BooleanField(
        default=False,
        verbose_name="Appointment Approval"
    )
    objects = AppointmentManager()

    class Meta:
        db_table = 'Appointments'


def post_user_save(sender,instance,**kwargs):
    if UserAppointmentPoint.objects.filter(user=instance).count() == 0:
        pointobject = UserAppointmentPoint()
        pointobject.user = instance
        pointobject.save()


post_save.connect(post_user_save,sender=HealthGuardUser)
