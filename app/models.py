from django.db import models
# from django.utils import timezone

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    manufacturer = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    ram = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    image = models.CharField(max_length=100)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "products"

    def __str__(self):
        return self.manufacturer + " - " + self.model


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "manufacturers"

    def __str__(self):
        return self.name














