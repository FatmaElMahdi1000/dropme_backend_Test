from django.contrib import admin
from .models import Deposit, RVM, Wallet

@admin.register(RVM)
class RVMAdmin(admin.ModelAdmin):
    list_display = ('id', 'location', 'ActiveORnot', 'last_connection')

@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ('user_id','user', 'material_type', 'weight', 'points_earned', 'created_at')
    #added this recently, 'user__username' must be added this way matching how username is written in Django's built in libraries
    search_fields = ('user__username', 'material_type')
    list_filter = ('material_type', 'machine')

#adding admin fields for wallet
@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user_id','user','balance') #list display must be a tuple not a string, so I added the comma

#if we've a module and we need to add it with nothing to display, in admin, we can just write below comment
#i changed Wallet interface to show "user" name and "balance" as above.
# admin.site.register(Wallet)