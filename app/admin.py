from django.contrib import admin

# Register your models here.
from .models import Product, Manufacturer, Category, Profile
admin.site.register(Product)
admin.site.register(Manufacturer)
admin.site.register(Category)
admin.site.register(Profile)