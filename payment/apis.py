from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from drf_spectacular.utils import extend_schema

from .models import *


@extend_schema()
class PaymentAPIView(APIView):
    def post(self, request, *args, **kwargs):
        payment = Payment(
            amount=request.data.get('amount'),
            currency=request.data.get('currency'),
            description=request.data.get('description'),
        )
        if payment.charge(request.data.get('token')):
            return Response({'success': True}, status=HTTP_200_OK)
        else:
            return Response({'success': False}, status=HTTP_400_BAD_REQUEST)
