from rest_framework import serializers
from .models import Customer, Order

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'address', 'joined_on']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['total_price']

    def create(self, validated_data):
        validated_data['total_price'] = validated_data['quantity'] * validated_data['price']
        return super().create(validated_data)
