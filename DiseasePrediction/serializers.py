from rest_framework import serializers
from .models import TestReport


class TestSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestReport
        fields = ['user', 'type', 'symptoms', 'result', 'chances', 'date']

    def save(self, **kwargs):

        report = TestReport.objects.new_test_report(
            user_email=self.validated_data['user'],
            t_type=self.validated_data['type'],
            symptoms=self.validated_data['symptoms'],
            result=self.validated_data['result'],
            chances=self.validated_data['chances'],
            date=self.validated_data['date']
        )
        return report
