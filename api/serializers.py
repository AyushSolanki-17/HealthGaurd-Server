from rest_framework import serializers
from MainWebApp.models import HealthGuardUser


class SignUpSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = HealthGuardUser
        fields = ['email', 'fname', 'mobile', 'gender', 'dob', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = HealthGuardUser(
            email=self.validated_data['email'],
            fname=self.validated_data['fname'],
            mobile=self.validated_data['mobile'],
            gender=self.validated_data['gender'],
            dob=self.validated_data['dob'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password and password2 and password != password2:
            raise serializers.ValidationError({'password': 'passwords must match'})

        user.set_password(password)
        user.save()
        return user
