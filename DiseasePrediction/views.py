from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .serializers import TestSerializer
import json
import os
import pickle
import numpy as np
from .MLmodels.description_generator import generate_report_description, generate_result, general_Result_Generator
# Create your views here.
modulePath = os.path.dirname(__file__)
Dengue_model = pickle.load(open(os.path.join(modulePath, 'MLmodels/Dengue/Dengue.sav'), 'rb'))
Chikungunya_model = pickle.load(open(os.path.join(modulePath, 'MLmodels/Chikungunya/Chikungunya.sav'), 'rb'))
General_model = pickle.load(open(os.path.join(modulePath, 'MLmodels/General/General.sav'), 'rb'))
Covid_model = pickle.load(open(os.path.join(modulePath, 'MLmodels/Covid/Covid.sav'), 'rb'))
Malaria_model = pickle.load(open(os.path.join(modulePath, 'MLmodels/Malaria/Malaria.sav'), 'rb'))


class DengueView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            symps = json.loads(request.data['symptoms'])
            per = Dengue_model.predict_proba(
                [[symps['fever'], symps['headache'], symps['rashes'],
                  symps['nvom'], symps['eyepain'], symps['musclepain'],
                  symps['jointpain'], symps['loa'], symps['fatigue'], symps['bleeding'],
                  symps['days']]])
            per = np.array(per)[0][1]
            if per == 1.:
                per = 100
            else:
                per = int(str(per)[2:4])
            result = generate_result(per, 'dengue')
            srdata = {
                'user': request.data['user'],
                'symptoms': request.data['symptoms'],
                'date': request.data['date'],
                'type': 'dengue',
                'result': result,
                'chances': per,
            }
            serializer = TestSerializer(data=srdata)
            if serializer.is_valid():
                report = serializer.save()
                data = {
                    'fname': report.user.fname,
                    'email': report.user.email,
                    'type': 'dengue',
                    'result': report.result,
                    'description': generate_report_description(report,'dengue'),
                }
                return Response(data)
            else:
                err = {
                    'Error': serializer.errors
                }
                return Response(err)
        except Exception as e:
            err = {
                    'Error': e
                }
            return Response(err)


class ChikungunyaView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            symps = json.loads(request.data['symptoms'])
            per = Chikungunya_model.predict_proba(
                [[symps['fever'], symps['headache'], symps['rashes'],
                  symps['musclepain'], symps['jointpain'], symps['fatigue'], symps['swelling'], symps['chronic'],
                  symps['days']]])
            per = np.array(per)[0][1]
            if per == 1.:
                per = 100
            else:
                per = int(str(per)[2:4])
            result = generate_result(per, 'chikungunya')
            srdata = {
                'user': request.data['user'],
                'symptoms': request.data['symptoms'],
                'date': request.data['date'],
                'type': 'chikungunya',
                'result': result,
                'chances': per,
            }
            serializer = TestSerializer(data=srdata)
            if serializer.is_valid():
                report = serializer.save()
                data = {
                    'fname': report.user.fname,
                    'email': report.user.email,
                    'type':'chikungunya',
                    'result': report.result,
                    'description': generate_report_description(report,'chikungunya'),
                }
                return Response(data)
            else:
                err = {
                    'Error': serializer.errors
                }
                return Response(err)
        except Exception as e:
            err = {
                    'Error': 'server error',
                }
            return Response(err)


class GeneralView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            symps = json.loads(request.data['symptoms'])
            per = General_model.predict(
                [[symps['fever'], symps['rashes'], symps['bleeding'],
                  symps['jointpain'], symps['vomiting'], symps['swelling'],
                  symps['cough'], symps['shivering'], symps['respiratory'],
                  symps['lossofsmell'], symps['sorethroat'], symps['days']]])
            per = per[0]
            result, desc = general_Result_Generator(per)
            srdata = {
                'user': request.data['user'],
                'symptoms': request.data['symptoms'],
                'date': request.data['date'],
                'type': 'general',
                'result': result,
                'chances': per,
            }
            serializer = TestSerializer(data=srdata)
            if serializer.is_valid():
                report = serializer.save()
                data = {
                    'fname': report.user.fname,
                    'email': report.user.email,
                    'type':'General',
                    'result': report.result,
                    'description': desc,
                }
                print(data)
                return Response(data)
            else:
                err = {
                    'Error': serializer.errors
                }
                print(serializer.errors)
                return Response(err)
        except Exception as e:
            err = {
                    'Error': 'server error',
                }
            print(err)
            return Response(err)


class CovidView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            symps = json.loads(request.data['symptoms'])
            per = Covid_model.predict_proba(
                [[symps['fever'], symps['cough'], symps['respiratory'],
                  symps['heartrate'], symps['pain'], symps['lossofsmell'],
                  symps['chronic'], symps['days']]])
            per = np.array(per)[0][1]
            if per == 1.:
                per = 100
            else:
                per = int(str(per)[2:4])
            result = generate_result(per, 'covid')
            srdata = {
                'user': request.data['user'],
                'symptoms': request.data['symptoms'],
                'date': request.data['date'],
                'type': 'covid',
                'result': result,
                'chances': per,
            }
            serializer = TestSerializer(data=srdata)
            if serializer.is_valid():
                report = serializer.save()
                data = {
                    'fname': report.user.fname,
                    'email': report.user.email,
                    'type':'covid',
                    'result': report.result,
                    'description': generate_report_description(report,'covid'),
                }
                return Response(data)
            else:
                err = {
                    'Error': serializer.errors
                }
                return Response(err)
        except Exception as e:
            err = {
                    'Error': 'server error',
                }
            return Response(err)


class MalariaView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            symps = json.loads(request.data['symptoms'])
            per = Malaria_model.predict_proba(
                [[symps['fever'], symps['headache'], symps['shivering'],
                  symps['vomiting'], symps['cough'], symps['respiratory'], symps['fastheartrate'], symps['fatigue'],
                  symps['chronic'], symps['days']]])
            per = np.array(per)[0][1]
            if per == 1.:
                per = 100
            else:
                per = int(str(per)[2:4])
            result = generate_result(per, 'malaria')
            srdata = {
                'user': request.data['user'],
                'symptoms': request.data['symptoms'],
                'date': request.data['date'],
                'type': 'malaria',
                'result': result,
                'chances': per,
            }
            serializer = TestSerializer(data=srdata)
            if serializer.is_valid():
                report = serializer.save()
                data = {
                    'fname': report.user.fname,
                    'email': report.user.email,
                    'type':'malaria',
                    'result': report.result,
                    'description': generate_report_description(report,'malaria'),
                }
                return Response(data)
            else:
                err = {
                    'Error': serializer.errors
                }
                return Response(err)
        except Exception as e:
            err = {
                    'Error': 'server error',
                }
            print(e)
            return Response(err)
