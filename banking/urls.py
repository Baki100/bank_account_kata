# banking/urls.py

from django.urls import path
from .views import DepositView, WithdrawView, TransferView, StatementView



urlpatterns = [
    path('deposit/', DepositView.as_view({'post': 'create'}), name='deposit'),
    path('withdraw/', WithdrawView.as_view({'post': 'create'}), name='withdraw'),
    path('transfer/', TransferView.as_view({'post': 'create'}), name='transfer'),
    path('statement/', StatementView.as_view({'get': 'list'}), name='statement'),
]


