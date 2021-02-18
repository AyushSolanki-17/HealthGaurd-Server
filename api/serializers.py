from rest_framework import serializers
from MainWebApp.models import HealthGuardUser, HealthGuardDoctor


class SignUpSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = HealthGuardUser
        fields = ['email', 'fname', 'mobile', 'gender', 'dob', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password and password2 and password != password2:
            raise serializers.ValidationError({'password': 'passwords must match'})

        user = HealthGuardUser.objects.create_user(
            email=self.validated_data['email'],
            fname=self.validated_data['fname'],
            mobile=self.validated_data['mobile'],
            gender=self.validated_data['gender'],
            dob=self.validated_data['dob'],
            password=password
        )
        return user


class DoctorRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = HealthGuardDoctor
        fields = ['user', 'qualification', 'speciality', 'license_pdf']

    def save(self, **kwargs):
        doctor = HealthGuardDoctor.objects.create_doctor(
            self.validated_data['user'],
            self.validated_data['qualification'],
            self.validated_data['speciality'],
            self.validated_data['license_pdf'],
        )
        return doctor
