"""
Only functional tests are defined here since there is no real need for Unit
tests.
"""
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase

from payments.models import Account


class AccountListTests(APITestCase):
    def test_get_empty(self):
        """
        Perform GET request when there are no existing accounts
        """
        response = self.client.get(reverse('account-list')).data

        self.assertEqual(response, [])

    def test_with_data(self):
        """
        Perform GET request and check results
        """
        bob_acc = Account(owner='Bob', currency='USD', balance=1000)
        bob_acc.save()
        alice_acc = Account(owner='Alice', currency='PHP', balance=800)
        alice_acc.save()

        response = self.client.get(reverse('account-list')).data

        self.assertEqual(len(response), 2)
        # check all fields are present
        self.assertIn('id', response[0])
        self.assertIn('id', response[1])
        self.assertIn('owner', response[0])
        self.assertIn('owner', response[1])
        self.assertIn('balance', response[0])
        self.assertIn('balance', response[1])
        # check content
        owners = map(lambda item: item['owner'], response)
        self.assertIn(bob_acc.owner, owners)
        self.assertIn(alice_acc.owner, owners)
