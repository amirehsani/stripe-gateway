from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from drf_spectacular.utils import extend_schema

from .models import *


@extend_schema(
    description='Process a payment using Stripe',
    request={
        'type': 'object',
        'properties': {
            'amount': {'type': 'string', 'format': 'decimal'},
            'currency': {'type': 'string'},
            'description': {'type': 'string'},
            'token': {'type': 'string'},
        },
        'required': ['amount', 'currency', 'description', 'token'],
    },
    responses={
        HTTP_200_OK: {'description': 'Payment processed successfully'},
        HTTP_400_BAD_REQUEST: {'description': 'Payment declined'},
    },
)
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
