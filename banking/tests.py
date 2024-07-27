# banking/tests.py

from django.test import TestCase
from .models import Account, Transaction

class AccountModelTests(TestCase):
    def setUp(self):
        self.account = Account.objects.create(
            account_number="123456",
            iban="GB29NWBK60161331926819",
            balance=1000.00
        )

    def test_account_balance(self):
        self.assertEqual(self.account.balance, 1000.00)

class TransactionModelTests(TestCase):
    def setUp(self):
        self.account = Account.objects.create(
            account_number="123456",
            iban="GB29NWBK60161331926819",
            balance=1000.00
        )
        self.transaction = Transaction.objects.create(
            account=self.account,
            type='deposit',
            amount=200.00
        )

    def test_transaction_creation(self):
        self.assertEqual(self.transaction.amount, 200.00)
        self.assertEqual(self.transaction.type, 'deposit')

