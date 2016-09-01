from django.contrib import admin
from payu.models import Transaction, CancelRefundCaptureRequests

# Register your models here.

admin.site.register(Transaction)
admin.site.register(CancelRefundCaptureRequests)
