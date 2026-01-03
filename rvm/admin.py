from django.contrib import admin
from .models import Deposit, RVM, Wallet

@admin.register(RVM)
class RVMAdmin(admin.ModelAdmin):
    list_display = ('location', 'ActiveORnot', 'last_connection')

@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ('user', 'material_type', 'weight', 'points_earned', 'created_at')
    list_filter = ('material_type', 'machine')

admin.site.register(Wallet)