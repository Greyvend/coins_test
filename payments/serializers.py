"""
Django Rest Framework serializers.
"""

from rest_framework import serializers

from payments.models import Account, Payment


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'owner', 'balance', 'currency')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'from_account', 'to_account', 'amount')
