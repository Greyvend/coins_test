"""
Defines models dealing with user accounts and payment transactions.
"""
from django.db import models


class Account(models.Model):
    owner = models.CharField(max_length=40)
    balance = models.IntegerField()
    currency = models.CharField(max_length=3)  # ISO 4217 standard name

    def __unicode__(self):
        return u'{}: {} {}'.format(self.owner, self.balance, self.currency)


class Payment(models.Model):
    from_account = models.ForeignKey(Account, related_name='outgoing_payments')
    to_account = models.ForeignKey(Account, related_name='incoming_payments')
    amount = models.IntegerField()

    def __unicode__(self):
        return u'Payment {} -> {}, for {}'.format(self.from_account,
                                                  self.to_account,
                                                  self.amount)
