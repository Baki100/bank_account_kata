# bank_account_kata/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/banking', include('banking.urls')),
]

