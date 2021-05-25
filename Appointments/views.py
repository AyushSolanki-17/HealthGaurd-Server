from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ClincsRetireveSerializer,AppointmentRequestSerializer
# Create your views here.


class ClinicsApi(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ClincsRetireveSerializer(data=request.data)
        if serializer.is_valid():
            jdata = serializer.getClinics()
            return Response(jdata)
        else:
            return Response(serializer.errors)


class AppointmentRequest(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = AppointmentRequestSerializer(data=request.data)
        if serializer.is_valid():
            appt = serializer.save()
            return Response(appt)
        else:
            return Response(serializer.errors)

