from rest_framework import serializers
from .models import Deposit

class DepositSerializer(serializers.ModelSerializer):
    # We mark points_earned as read_only so a user cannot send
    points_earned = serializers.ReadOnlyField()

    class Meta:
        model = Deposit
        # These are the fields the "Translator/Serializer" will look for in the JSON
        fields = ['id', 'material_type', 'weight', 'machine_id', 'points_earned', 'created_at']

    def create(self, validated_data):

        material = validated_data.get('material_type').upper()
        weight = validated_data.get('weight')

        rates = {
            'PLASTIC': 1,  # 1 point/kg
            'METAL': 3,    # 3 points/kg
            'GLASS': 2     # 2 points/kg
        }

        #Calculating points: Weight * Rate
        points = weight * rates.get(material, 0)

        validated_data['points_earned'] = points

        return Deposit.objects.create(**validated_data)