from django.urls import path
from . import views

app_name = 'DiseasePrediction'

urlpatterns = [
    path('dengue/', views.DengueView.as_view()),
    path('chikungunya/', views.ChikungunyaView.as_view()),
]

