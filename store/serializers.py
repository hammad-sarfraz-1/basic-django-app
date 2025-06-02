from rest_framework import serializers

from .models import Customer, Order, Product


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "joined_on",
        ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "stock"]


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField()
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)
    total_price = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "product",  # Added 'product'
            "quantity",
            "status",
            "total_price",
            "created_at",
        ]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value

    def create(self, validated_data):
        # Auto-calculate total_price based on product.price and quantity
        product = validated_data["product"]
        quantity = validated_data["quantity"]
        validated_data["total_price"] = product.price * quantity
        return super().create(validated_data)
