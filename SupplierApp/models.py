from django.contrib.auth.models import User
from django.db import models


class Supplier(models.Model):
    name = models.TextField(max_length=100)
    location = models.TextField(max_length=200)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class AHPcalculation(models.Model):
    user = models.ForeignKey(
        User, verbose_name="user", on_delete=models.CASCADE)
    supplier = models.ForeignKey(
        Supplier, verbose_name="supplier", on_delete=models.CASCADE)
    results = models.DecimalField(max_digits=10, decimal_places=4)
    ranking = models.IntegerField()

    def __str__(self):
        return str(self.ranking)


class Criteria(models.Model):
    supplier_id = models.ForeignKey(
        Supplier, verbose_name="supplier", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    quality = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    delivery = models.DateField()
    credibility = models.CharField(max_length=20)
    license = models.BooleanField()
    distance = models.DecimalField(max_digits=10, decimal_places=4)
    shipping_fees = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return self.supplier_id


class Weights(models.Model):
    criteria_id = models.ForeignKey(
        Criteria, verbose_name="criteria", on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return str(self.value)


class BenefitCost(models.Model):
    criteria_id = models.ForeignKey(
        Criteria, verbose_name="criteria", on_delete=models.CASCADE)
    benefit = models.TextField()
    cost = models.TextField()

    def __str__(self):
        return str(self.criteria_id)