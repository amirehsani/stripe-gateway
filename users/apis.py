from abc import ABC

from rest_framework import serializers
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from .models import BaseUser


class RegisterAPI(APIView):

    class InputSerializer(serializers.Serializer, ABC):
        email = serializers.EmailField(max_length=255)
        password = serializers.CharField(max_length=100)
        confirm_password = serializers.CharField(max_length=100)

    class OutputSerializer(serializers.Serializer):
        class Meta:
            model = BaseUser
            fields = 'email'

    @extend_schema(request=InputSerializer, responses=OutputSerializer)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            query = create_user(
                email = serializer.validated_data.get('email'),
                password = serializers.validated_data.get('password')
            )

        except Exception as x:
            return Response(
                f"Database Error {x}", status=HTTP_400_BAD_REQUEST
            )

        return Response(self.OutputSerializer(query, context={'request': request}).data)















# from django.core.validators import MinLengthValidator
# from rest_framework import serializers
# from rest_framework.views import APIView
#
# from .models import BaseUser
# from common.validators import *
#
#
# class RegisterApi(APIView):
#
#     class InputRegisterSerializer(serializers.Serializer):
#         email = serializers.EmailField(max_length=255)
#         bio = serializers.CharField(max_length=1000, required=False)
#         password = serializers.CharField(
#             validators=[
#                 number_validator, letter_validator, special_char_validator,
#                 MinLengthValidator(limit_value=10)
#             ]
#         )
#
#         confirm_password = serializers.CharField(max_length=255)
#
#         @staticmethod
#         def validate_email(email):
#             if BaseUser.objects.filter(email=email).exists():
#                 raise serializers.ValidationError("email Already Taken")
#             return email
#
#         def validate(self, data):
#             if not data.get("password") or not data.get("confirm_password"):
#                 raise serializers.ValidationError("Please fill password and confirm password")
#
#             if data.get("password") != data.get("confirm_password"):
#                 raise serializers.ValidationError("confirm password is not equal to password")
#             return data
