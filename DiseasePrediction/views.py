from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .serializers import TestSerializer
import json
import os
import pickle
import numpy as np
# Create your views here.
modulePath = os.path.dirname(__file__)
Dengue_model = pickle.load(open(os.path.join(modulePath, 'MLmodels/Dengue/Dengue.sav'), 'rb'))
Chikungunya_model = pickle.load(open(os.path.join(modulePath, 'MLmodels/Chikungunya/Chikungunya.sav'), 'rb'))


def generate_report_description(report,disease):
    desc = ''
    if report.chances >= 75:
        desc += f'According to our system you have very high chances of having {disease}. ' \
                  'You must consult your nearby healthcare institue or doctor as soon as possible and take steps' \
                  'according to he/she says. '
    elif 50 <= report.chances < 75:
        desc += f'According to our system you have chances of having {disease}. ' \
                  'No need to fear or panic a lot. ' \
                  'Please consult your nearby healthcare institue or doctor as soon as possible for proper reports ' \
                  'and testsand take steps according to he/she says. '
    elif 35 <= report.chances < 50:
        desc += f'According to our system you have low chances of having {disease}. ' \
                  f'No need to fear or panic a lot. You are looking fine with less effective symptoms of {disease}. ' \
                  'But if you are not feeling well then please consult your nearby healthcare institue or ' \
                  'doctor as soon as possible for proper reports and testsand take steps according to he/she says. '
    else:
        desc += f'According to our system you are safe from {disease}. You are looking fine with less ' \
                  f'effective symptoms of {disease}. You might have a normal flue so no need to have high tensisons '
    symptoms = report.symptoms.split(',')
    s_count = len(symptoms)
    desc += f' You face {s_count} ' \
            f'recognized symptoms of {report.type} which are {report.symptoms}. ' \
            f'According to our system you have {report.chances}% chance of being ' \
            f'affected of {report.type}. '
    return desc


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
            if per >= 75:
                result = 'Very high dengue positive chances.'
            elif 50 <= per < 75:
                result = 'High dengue positive chances'
            elif 35 <= per < 50:
                result = 'Low dengue positive chances'
            else:
                result = 'Safe from dengue'
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
            if per >= 75:
                result = 'Very high chikungunya positive chances.'
            elif 50 <= per < 75:
                result = 'High chikungunya positive chances'
            elif 35 <= per < 50:
                result = 'Low chikungunya positive chances'
            else:
                result = 'Safe from chikungunya'
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
