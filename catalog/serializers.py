from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "price_idr", "price_sgd", "created_at", "updated_at"]

    def validate_price_idr(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value
