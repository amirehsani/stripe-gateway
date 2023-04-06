from abc import ABC

from django.core.validators import MinLengthValidator
from rest_framework import serializers
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from common.validators import *
from .services import register
from .selectors import get_profile
from .models import BaseUser, Profile


# USER REGISTRATION API -----------------------------
class RegisterAPI(APIView):
    class InputRegisterSerializer(serializers.Serializer):
        email = serializers.EmailField(max_length=255)
        country = serializers.CharField(max_length=100)
        password = serializers.CharField(validators=[
            number_validator,
            letter_validator,
            special_char_validator,
            MinLengthValidator(limit_value=8),
        ])
        confirm_password = serializers.CharField(max_length=100)

    def validate_email(self, email):
        if BaseUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email is already taken")
        return email

    def validate(self, data):
        if not data.get("password") or not data.get("confirm_password"):
            raise serializers.ValidationError("Please fill password and confirm password")

        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError("confirm password is not equal to password")
        return data

    class OutputRegisterSerializer(serializers.Serializer):
        class Meta:
            model = BaseUser
            fields = ('email', 'created_at', 'updated_at')

    @extend_schema(request=InputRegisterSerializer, responses=OutputRegisterSerializer)
    def post(self, request):
        serializer = self.InputRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = register(
                email=serializer.validated_data.get('email'),
                password=serializer.validated_data.get('password'),
                country=serializer.validated_data.get('country'),
            )

        except Exception as x:
            return Response(
                f"Database Error {x}", status=HTTP_400_BAD_REQUEST
            )

        return Response(self.OutputRegisterSerializer(user, context={'request': request}).data)


# USER PROFILE API ------------------------
class ProfileAPI(APIView):

    class OutputProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = ('user', 'country')

    @extend_schema(responses=OutputProfileSerializer)
    def get(self, request):
        query = get_profile(user=request.user)
        return Response(self.OutputProfileSerializer(query, context={'request': request}).data)
