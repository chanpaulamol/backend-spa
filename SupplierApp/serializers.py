from rest_framework import serializers
from .models import Supplier,  Ranking
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['password', 'username', 'first_name', 'last_name',
                  'email', 'is_staff', 'is_active', 'date_joined']


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['name', 'financial_status', 'quality', 'service', 'reputation',
                  'technical_capability', 'price_cost']


class RankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ranking
        fields = ['supplier_name', 'results', 'ranking']
