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
    #one user can have one wallet One to one relationship 1 - 1
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default='0.00')
    def __str__(self):
        return f"{self.user.username}'s Wallet"


class Deposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deposits')
    #it means many deposits can occur in one RVM - One to many relation.
    machine = models.ForeignKey(RVM, on_delete=models.SET_NULL, null=True, related_name='activities')

    # automatically sets the timestamp when deposit is made
    created_at = models.DateTimeField(auto_now_add=True)

    # IdemPotent Logic(class Meta): Reps does not change the value; Preventing our server from adding the same request twice in case the machine retries
    # sending the same request twice due to a glitch or sth.
    class Meta:
        unique_together = ('user', 'machine', 'created_at')

    MATERIAL_CHOICES = [
        ('PLASTIC', 'Plastic'),
        ('METAL', 'Metal'),
        ('GLASS', 'Glass'),
    ]
    material_type = models.CharField(max_length=10, choices=MATERIAL_CHOICES)
    weight = models.FloatField()
    points_earned = models.FloatField(default=0.0)
    def save(self, *args, **kwargs):
        rates = {
            'PLASTIC': Decimal('1.0'),
            'METAL': Decimal('3.0'),
            'GLASS': Decimal('2.0')
        }

        calc_points = Decimal(str(self.weight)) * rates.get(self.material_type.upper(), Decimal('0.0'))
        self.points_earned = float(calc_points)


        super().save(*args, **kwargs)

        wallet, created = Wallet.objects.get_or_create(user=self.user)
        wallet.balance = Decimal(str(wallet.balance)) + calc_points
        wallet.save()