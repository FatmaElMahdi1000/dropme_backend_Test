from rest_framework import serializers
from .models import Deposit

class DepositSerializer(serializers.ModelSerializer):
    # We mark points_earned as read_only so a user cannot send
    # their own point value in the request.
    points_earned = serializers.ReadOnlyField()

    class Meta:
        model = Deposit
        # These are the fields the "Translator" will look for in the JSON
        fields = ['id', 'material_type', 'weight', 'machine_id', 'points_earned', 'created_at']

    def create(self, validated_data):
        """
        This method runs when we save a new deposit.
        It's the perfect place for our calculation logic.
        """
        # 1. Extract the data from the validated request
        material = validated_data.get('material_type').upper()
        weight = validated_data.get('weight')

        # 2. Define our reward rates (The logic from your task)
        rates = {
            'PLASTIC': 1,  # 1 point/kg
            'METAL': 3,    # 3 points/kg
            'GLASS': 2     # 2 points/kg
        }

        # 3. Calculate points: Weight * Rate
        # .get() is safe—it defaults to 0 if the material is unknown
        points = weight * rates.get(material, 0)

        # 4. Attach the calculated points to the data before it hits the Database
        validated_data['points_earned'] = points

        # 5. Create the record in the database
        return Deposit.objects.create(**validated_data)