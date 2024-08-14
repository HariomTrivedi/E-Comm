# shop/serializers.py
from rest_framework import serializers
from .models import Product, Contact, Orders, orderUpdate

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'

class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = orderUpdate
        fields = '__all__'
