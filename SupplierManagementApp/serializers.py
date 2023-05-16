from rest_framework import serializers
from .models import Supplier, AHPcalculation, Criteria, Weights, BenefitCost


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['name', 'location', 'email', 'phone_number']


class AHPcalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AHPcalculation
        fields = ['supplier', 'results', 'ranking']


class CriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criteria
        fields = ['product_name', 'price',
                  'delivery_time', 'cost', 'distance']


class WeightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weights
        fields = ['criteria_id', 'value']


class BenefitCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BenefitCost
        fields = ['criteria_id', 'benefit', 'cost']
