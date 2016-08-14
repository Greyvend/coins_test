"""
Only functional tests are defined here since there is no real need for Unit
tests.
"""
from unittest.mock import patch

from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase

from payments.models import Account, Payment


class AccountListTests(APITestCase):
    def test_get_empty(self):
        """
        Perform GET request when there are no existing accounts
        """
        response = self.client.get(reverse('account-list')).data

        self.assertEqual(response, [])

    def test_get_with_data(self):
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


class PaymentListTests(APITestCase):
    def test_get_empty(self):
        """
        Perform GET request when there are no existing accounts
        """
        response = self.client.get(reverse('account-list')).data

        self.assertEqual(response, [])

    def test_get_with_data(self):
        """
        Perform GET request and check results
        """
        bob_acc = Account(owner='Bob', currency='USD', balance=1000)
        bob_acc.save()
        alice_acc = Account(owner='Alice', currency='PHP', balance=800)
        alice_acc.save()
        bob_to_alice = Payment(from_account=bob_acc, to_account=alice_acc,
                               amount=500)
        bob_to_alice.save()
        alice_to_bob = Payment(from_account=bob_acc, to_account=alice_acc,
                               amount=400)
        alice_to_bob.save()

        response = self.client.get(reverse('payment-list')).data

        self.assertEqual(len(response), 2)
        # check all fields are present
        self.assertIn('id', response[0])
        self.assertIn('id', response[1])
        self.assertIn('from_account', response[0])
        self.assertIn('from_account', response[1])
        self.assertIn('to_account', response[0])
        self.assertIn('to_account', response[1])
        self.assertIn('amount', response[1])
        self.assertIn('amount', response[1])
        # check content
        amounts = map(lambda item: item['amount'], response)
        self.assertIn(bob_to_alice.amount, amounts)
        self.assertIn(alice_to_bob.amount, amounts)

    def test_post_same_currency(self):
        """
        Perform POST request to create payment in case both users have same
        currency settings. Verify that balances change appropriately and new
        payment row is created in DB.
        """
        bob_acc = Account(owner='Bob', currency='USD', balance=1000)
        bob_acc.save()
        alice_acc = Account(owner='Alice', currency='USD', balance=800)
        alice_acc.save()

        response = self.client.post(reverse('payment-list'),
                                    data={'from_account': bob_acc.id,
                                          'to_account': alice_acc.id,
                                          'amount': 500}).data

        self.assertTrue(isinstance(response, dict))
        # check all fields of created model are present
        self.assertEqual(response['id'], 1)
        self.assertEqual(response['from_account'], bob_acc.id)
        self.assertEqual(response['to_account'], alice_acc.id)
        self.assertEqual(response['amount'], 500)
        # check that Payment model was created
        payments = Payment.objects.all()
        self.assertEqual(len(payments), 1)
        self.assertEqual(payments[0].id, 1)
        self.assertEqual(payments[0].from_account.id, bob_acc.id)
        self.assertEqual(payments[0].to_account.id, alice_acc.id)
        self.assertEqual(payments[0].amount, 500)
        # finally check that accounts were charged appropriately
        bob_acc.refresh_from_db()
        self.assertEqual(bob_acc.balance, 500)
        alice_acc.refresh_from_db()
        self.assertEqual(alice_acc.balance, 1300)

    def test_post_different_currency_mocked(self):
        """
        Perform POST request to create payment in case users have different
        currency settings. Verify that balances change appropriately and new
        payment row is created in DB. API request to third party API is mocked.
        """
        bob_acc = Account(owner='Bob', currency='USD', balance=1000)
        bob_acc.save()
        alice_acc = Account(owner='Alice', currency='PHP', balance=800)
        alice_acc.save()

        with patch('payments.views.convert', autospec=True) as mock_convert:
            mock_convert.return_value = 2329
            self.client.post(reverse('payment-list'),
                             data={'from_account': bob_acc.id,
                                   'to_account': alice_acc.id,
                                   'amount': 50})

        # check that accounts were charged appropriately
        bob_acc.refresh_from_db()
        self.assertEqual(bob_acc.balance, 950)
        alice_acc.refresh_from_db()
        self.assertEqual(alice_acc.balance, 3129)
