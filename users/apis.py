from abc import ABC

from django.core.validators import MinLengthValidator
from rest_framework import serializers
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema


from common.validators import *
from .services import create_user, register
from .selectors import get_profile
from .models import BaseUser, Profile


# USER REGISTRATION API -----------------------------
class RegisterAPI(APIView):

    class InputSerializer(serializers.Serializer, ABC):
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

    class OutputSerializer(serializers.Serializer):
        class Meta:
            model = BaseUser
            fields = 'email'

    @extend_schema(request=InputSerializer, responses=OutputSerializer)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            query = register(
                email = serializer.validated_data.get('email'),
                password = serializers.validated_data.get('password'),
                country = serializers.validated_data.get('country'),
            )

        except Exception as x:
            return Response(
                f"Database Error {x}", status=HTTP_400_BAD_REQUEST
            )

        return Response(self.OutputSerializer(query, context={'request': request}).data)


# USER PROFILE API ------------------------
class ProfileAPI(APIView):

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = ('user', 'date_of_birth', 'country')

    @extend_schema(responses=OutputSerializer)
    def get(self, request):
        query = get_profile(user=request.user)
        return Response(self.OutputSerializer(query, context= {'request': request},
                                              many=True).data)
