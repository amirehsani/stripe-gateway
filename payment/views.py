import stripe

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import *

# STRIPE_SK = .keysstripe.api_key


class PaymentAPIView(APIView):
    def post(self, request, *args, **kwargs):
        payment = Payment(
            amount=request.data.get('amount'),
            currency=request.data.get('currency'),
            description=request.data.get('description'),
        )
        if payment.charge(request.data.get('token')):
            return Response({'success': True}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)
