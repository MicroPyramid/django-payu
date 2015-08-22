from django.contrib import admin
from models import Transaction, CancelRefundCaptureRequests

# Register your models here.

admin.site.register(Transaction)
admin.site.register(CancelRefundCaptureRequests)
