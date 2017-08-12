from django.contrib.auth import authenticate, password_validation
from .models import User
from rest_framework import serializers
from simple_email_confirmation.models import EmailAddress


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            username = validated_data['username'],
            password = validated_data['password'],
            is_active = False
        )
        return user

    def validate_email(self, value):
        if EmailAddress.objects.filter(email=value).count() > 0:
            raise serializers.ValidationError('Пользователь с таким email уже существует')
        return value

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def auth(self):
        user = authenticate(
            username=self.validated_data['username'],
            password=self.validated_data['password']
        )
        return user


class UserInfoSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        return {
            'username': obj.username,
            'email': obj.get_primary_email()
        }


class ConfirmEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_key = serializers.CharField()

    def create(self):
        user = User.objects.get(email=self.validated_data['email'])
        address = user.email_address_set.confirm(self.validated_data['confirmation_key'])
        user.is_active = True
        user.save()
        return address.email


