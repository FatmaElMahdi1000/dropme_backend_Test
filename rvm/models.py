from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
#the machine
class RVM(models.Model):
    location= models.CharField(max_length=400)
    ActiveORnot= models.BooleanField(default=True)
    last_connection= models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"The Machine's Location:{self.location}"

class Wallet(models.Model):
    #one user can have one wallet
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    def __str__(self):
        return f"{self.user.username}'s Wallet"

class Deposit(models.Model):
    #every entry in this class will be a column, column name will be for ex: user, MATERIAL_CHOICES, material_type, weight, etc.
    #class is the table itself.

    #many to one; A user can make several deposits
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deposits')
    machine = models.ForeignKey(RVM, on_delete=models.SET_NULL, null=True, related_name='activities')

    MATERIAL_CHOICES = [
        ('PLASTIC', 'Plastic'),
        ('METAL', 'Metal'),
        ('GLASS', 'Glass'),
    ]
    material_type = models.CharField(max_length=10, choices=MATERIAL_CHOICES) #max_length:how many chars in the cell, restricted to: MATERIAL_CHOICES

    weight = models.FloatField()  # stores weight in float(type) that's coming from the RVM,machine( 2.5 (kg))
    # machine_id = models.CharField(max_length=50)

    points_earned = models.FloatField(default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        rates = {
            'PLASTIC': 1,  # 1 point/kg
            'METAL': 3,  # 3 points/kg
            'GLASS': 2  # 2 points/kg
        }

        self.points_earned = self.weight * rates.get(self.material_type.upper(), 0)

        super().save(*args, **kwargs)
        #wallet balance update
        wallet, created = Wallet.objects.get_or_create(user=self.user)
        wallet.balance += Decimal(str(self.points_earned))
        wallet.save()