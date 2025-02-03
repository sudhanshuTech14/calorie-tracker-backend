from rest_framework import serializers
from .models import Food, Consume

class FoodSerializer(serializers.ModelSerializer):
    # calories = serializers.ReadOnlyField()  # Read-only since it's calculated

    class Meta:
        model = Food
        fields = '__all__'

class ConsumeSerializer(serializers.ModelSerializer):
    food_consumed = FoodSerializer(read_only=True)  # Nested representation
    food_consumed_id = serializers.PrimaryKeyRelatedField(
        queryset=Food.objects.all(), source='food_consumed', write_only=True
    )

    class Meta:
        model = Consume
        fields = ['id', 'user', 'food_consumed', 'food_consumed_id', 'quantity', 'date_consumed']
        read_only_fields = ['user']  # Ensure user is automatically set by the backend
