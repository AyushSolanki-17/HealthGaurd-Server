from django.urls import path, include
from . import views
app_name = 'Appointments'

urlpatterns = [
    path('clinics/',views.ClinicsApi.as_view()),
    path('request/',views.AppointmentRequest.as_view())
]