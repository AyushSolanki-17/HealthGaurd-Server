from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import FileUploadParser, MultiPartParser,FormParser
from rest_framework.response import Response
from .serializers import SignUpSerializer, DoctorRegisterSerializer
from rest_framework.views import APIView
from MainWebApp.models import HealthGuardUser
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
                'fname': user.fname,
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
        try:
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
            user = HealthGuardUser.objects.get(email=request.data['email'])
            resp = {
                'email': user.email,
                'fname': user.fname,
                'access_token': r.json()['access_token'],
                'refresh_token': r.json()['refresh_token']
                }
            return Response(resp)
        except:
            resp = {
                'Error': "Wrong password or email",
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
        user = HealthGuardUser.objects.get(email=request.data['email'])
        rs = r.json()
        resp = {
            'email': user.email,
            'fname': user.fname,
            'access_token': rs['access_token'],
            'refresh_token': rs['refresh_token']
            }
        return Response(resp)


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


class DoctorRegisterApi(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)

    def put(self, request, format=None):
        try:
            serializer = DoctorRegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                resp = {
                    'response': 'Successfully Applied to be registered as Doctor'
                }
                return Response(resp)
            else:
                return Response({
                    'err': serializer.errors
                })
        except Exception as e:
            print(e)
            return Response({
                'err': 'There is some problem with server!! try again later..!!',
            })

