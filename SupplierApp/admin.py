from django.contrib import admin
from .models import Supplier, Ranking


class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'financial_status', 'quality', 'service',
                    'reputation', 'technical_capability', 'price_cost']


class AHPcalculationAdmin(admin.ModelAdmin):
    list_display = ('supplier_name', 'results', 'ranking')


admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Ranking, AHPcalculationAdmin)
