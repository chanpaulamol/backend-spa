from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    financial_status = models.IntegerField()
    quality = models.IntegerField()
    service = models.IntegerField()
    reputation = models.IntegerField()
    technical_capability = models.IntegerField()
    price_cost = models.IntegerField()

    def __str__(self):
        return self.name


class Ranking(models.Model):
    supplier_name = models.CharField(max_length=150)
    results = models.DecimalField(max_digits=10, decimal_places=4)
    ranking = models.IntegerField()

    def __str__(self):
        return self.supplier_name
