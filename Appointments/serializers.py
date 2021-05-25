from abc import ABC

from rest_framework import serializers
from .models import Clinic, Appointment
import json


class ClincsRetireveSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=100)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def getClinics(self):
        c = self.validated_data['city']
        c = str(c).capitalize()
        clinics = Clinic.objects.filter(city=c)
        j = [{"doctor": obj.doctor.user.fname,
              "specialist": obj.doctor.speciality,
              "address": obj.address} for obj in clinics]
        return j


class AppointmentRequestSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=100)
    clinic = serializers.IntegerField()
    dt = serializers.CharField(max_length=25)

    def save(self, **kwargs):
        appt = Appointment.objects.appointment_request(
            user_email= self.validated_data['user'],
            clinicId= self.validated_data['clinic'],
            dt=self.validated_data['dt']
        )
        return appt
