from django.db import models
from django.contrib.auth.models import User

class Deposit(models.Model):
    #every entry in this class will be a column, column name will be for ex: user, MATERIAL_CHOICES, material_type, weight, etc.
    #class is the table itself.

    MATERIAL_CHOICES = [
        ('PLASTIC', 'Plastic'),
        ('METAL', 'Metal'),
        ('GLASS', 'Glass'),
    ]
    material_type = models.CharField(max_length=10, choices=MATERIAL_CHOICES) #max_length:how many chars in the cell, restricted to: MATERIAL_CHOICES

    weight = models.FloatField()  # stores weight in float(type) that's coming from the RVM,machine( 2.5 (kg))
    machine_id = models.CharField(max_length=50)

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