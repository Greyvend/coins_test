from django.http import HttpResponse
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
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
        return self.create(request, *args, **kwargs)