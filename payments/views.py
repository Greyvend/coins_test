from django.http import HttpResponse
from forex_python.converter import convert
from rest_framework import generics
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from payments.models import Account, Payment
from payments.serializers import AccountSerializer, PaymentSerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class AccountList(generics.ListAPIView):
    """
    List all accounts
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class PaymentList(generics.ListCreateAPIView):
    """
    List all payments and allow creating new payments
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        """
        POST request to create `Payment` model.

        Prime business logic. Charge souce user account and load funds to the
        destination account. Return `HTTP 422 Unprocessable Entity` in case
        source account doesn't have enough funds.
        ---
        parameters:
            - name: from_account
              type: integer
              required: true
              description: Source account PK
            - name: to_account
              type: integer
              required: true
              description: Destination account PK
            - name: amount
              type: integer
              required: true
              description: amount of funds to send, in source account's
                currency

        :return: created `Payment` object data
        """
        from_account = Account.objects.get(id=request.data['from_account'])
        to_account = Account.objects.get(id=request.data['to_account'])
        charge_amount = int(request.data['amount'])
        if from_account.balance < charge_amount:
            return Response('Insufficient balance.',
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if from_account.currency != to_account.currency:
            load_amount = convert(from_account.currency, to_account.currency,
                                  charge_amount)
        else:
            load_amount = charge_amount
        from_account.balance -= charge_amount
        to_account.balance += load_amount
        from_account.save()
        to_account.save()
        return self.create(request, *args, **kwargs)
