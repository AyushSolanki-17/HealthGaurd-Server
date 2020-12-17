from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import SignUpSerializer
from django.conf import settings
from oauth2_provider.models import AccessToken
from rest_framework.views import APIView
from HealthGuard.site_credentials import URL_LINK, CLIENT_ID, CLIENT_SECRET
import requests


class RegisterApi(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = {
                'grant_type': 'password',
                'username': user.email,
                'password': request.POST['password'],
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
            }
            r = requests.post(URL_LINK+'/o/token/', data=data)
            resp = {
                'email': user.email,
                'access_token': r.json()['access_token'],
                'refresh_token': r.json()['refresh_token']
            }
            return Response(resp)
        else:
            err = {
                'Error': serializer.errors
            }
            return Response(err)


class TokenApi(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        r = requests.post(
            URL_LINK+'/o/token/',
            data={
                'grant_type': 'password',
                'username': request.data['email'],
                'password': request.data['password'],
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
            },
        )
        resp = {
            'email': request.data['email'],
            'access_token': r.json()['access_token'],
            'refresh_token': r.json()['refresh_token']
            }
        return Response(resp)


class RefreshTokenApi(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        r = requests.post(
            URL_LINK+'/o/token/',
            data={
                'grant_type': 'refresh_token',
                'refresh_token': request.data['refresh_token'],
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
            },
        )
        return Response(r.json())


class RevokeTokenApi(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        r = requests.post(
            URL_LINK+'/o/revoke_token/',
            data={
                'token': request.data['token'],
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
            },
        )
        if r.status_code == requests.codes.ok:
            return Response({'message': 'token revoked'}, r.status_code)
        return Response(r.json(), r.status_code)



