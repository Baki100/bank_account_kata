# banking/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer
import re

IBAN_REGEX = re.compile(r'^[A-Z]{2}\d{2}[A-Z0-9]{1,30}$')

def is_valid_iban(iban):
    """Validate the IBAN format using a regex."""
    return IBAN_REGEX.match(iban) is not None


class DepositView(viewsets.ViewSet):
    def create(self, request):
        account_number = request.data.get('account_number')
        amount = request.data.get('amount')

        if not account_number or not amount:
            return Response({'error': 'Account number and amount are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = float(amount)
        except ValueError:
            return Response({'error': 'Invalid amount format. Must be a number.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            account = Account.objects.get(account_number=account_number)
            account.balance += amount
            account.save()

            transaction = Transaction.objects.create(
                account=account,
                type='deposit',
                amount=amount,
                description='Deposit made'
            )

            return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

class WithdrawView(viewsets.ViewSet):
    def create(self, request):
        account_number = request.data.get('account_number')
        amount = request.data.get('amount')

        if not account_number or not amount:
            return Response({'error': 'Account number and amount are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = float(amount)
        except ValueError:
            return Response({'error': 'Invalid amount format. Must be a number.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            account = Account.objects.get(account_number=account_number)
            if account.balance < amount:
                return Response({'error': 'Insufficient funds.'}, status=status.HTTP_400_BAD_REQUEST)

            account.balance -= amount
            account.save()

            transaction = Transaction.objects.create(
                account=account,
                type='withdraw',
                amount=amount,
                description='Withdrawal made'
            )

            return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

class TransferView(viewsets.ViewSet):
    def create(self, request):
        from_account_number = request.data.get('from_account_number')
        to_account_number = request.data.get('to_account_number')
        amount = request.data.get('amount')

        if not from_account_number or not to_account_number or not amount:
            return Response({'error': 'From account, to account, and amount are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = float(amount)
        except ValueError:
            return Response({'error': 'Invalid amount format. Must be a number.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from_account = Account.objects.get(account_number=from_account_number)
            to_account = Account.objects.get(account_number=to_account_number)

            if from_account.balance < amount:
                return Response({'error': 'Insufficient funds.'}, status=status.HTTP_400_BAD_REQUEST)

            from_account.balance -= amount
            to_account.balance += amount

            from_account.save()
            to_account.save()

            Transaction.objects.create(
                account=from_account,
                type='withdraw',
                amount=amount,
                description=f'Transfer to {to_account_number}'
            )

            Transaction.objects.create(
                account=to_account,
                type='deposit',
                amount=amount,
                description=f'Transfer from {from_account_number}'
            )

            return Response({'message': 'Transfer successful'}, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({'error': 'One or both accounts not found'}, status=status.HTTP_404_NOT_FOUND)

class StatementView(viewsets.ViewSet):
    def list(self, request):
        account_number = request.query_params.get('account_number')
        order = request.query_params.get('order', 'desc')

        if not account_number:
            return Response({'error': 'Account number is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            account = Account.objects.get(account_number=account_number)
            transactions = account.transaction_set.all()

            if order == 'asc':
                transactions = transactions.order_by('timestamp')
            else:
                transactions = transactions.order_by('-timestamp')

            return Response(TransactionSerializer(transactions, many=True).data, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

