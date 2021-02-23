from django.urls import path
from . import views

app_name = 'DiseasePrediction'

urlpatterns = [
    path('dengue/', views.DengueView.as_view()),
    path('chikungunya/', views.ChikungunyaView.as_view()),
    path('general/', views.GeneralView.as_view()),
    path('malaria/', views.MalariaView.as_view()),
    path('covid/', views.CovidView.as_view()),
]

