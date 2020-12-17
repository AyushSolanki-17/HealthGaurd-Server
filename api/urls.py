from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path('register/', views.RegisterApi.as_view(), name='register'),
    path('token/', views.TokenApi.as_view(), name='token'),
    path('token/refresh/', views.RefreshTokenApi.as_view(), name='refresh'),
    path('token/revoke/', views.RevokeTokenApi.as_view(), name='revoke'),
]
