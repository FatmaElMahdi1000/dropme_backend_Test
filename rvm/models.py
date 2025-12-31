from django.db import models
from django.contrib.auth.models import User

class Deposit(models.Model):
    # 1. Link to a User (If user is deleted, delete their deposits too)
    #every entry in this class will be a column, column name will be for ex: user, MATERIAL_CHOICES, material_type, weight, etc.
    # user = models.ForeignKey(User, on_object=models.CASCADE, related_name='deposits')
    #class is the table itself.

    MATERIAL_CHOICES = [
        ('PLASTIC', 'Plastic'),
        ('METAL', 'Metal'),
        ('GLASS', 'Glass'),
    ]
    material_type = models.CharField(max_length=10, choices=MATERIAL_CHOICES) #max_length:how many chars in the cell, restricted to: MATERIAL_CHOICES

    # 3. Data from the machine
    weight = models.FloatField()  # stores weight in float(type) that's coming from the RVM,machine( 2.5 (kg))
    machine_id = models.CharField(max_length=50)

    # 4. The result of our logic
    points_earned = models.FloatField(default=0.0)

    # 5. Timestamp (Good practice for any record)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        rates = {
            'PLASTIC': 1,  # 1 point/kg
            'METAL': 3,  # 3 points/kg
            'GLASS': 2  # 2 points/kg
        }

        self.points_earned = self.weight * rates.get(self.material_type.upper(), 0)

        super().save(*args, **kwargs)