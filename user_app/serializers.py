from rest_framework import serializers
from .models import *

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    def validate_email(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Користувач з таким email вже існує')
        return value

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError('Паролі не збігаються')
        attrs.pop('confirm_password')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        Profile.objects.create(user=user)
        return user

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password']

class MeSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Profile
        fields = ['country', 'country_code', 'city', 'lat', 'lng', 'email']