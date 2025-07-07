from django.db import models
from django.conf import settings

class Restaurant(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='restaurant')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    contacts = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='categories')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    photo = models.ImageField(upload_to='menu_items/', null=True, blank=True)
    is_hit = models.BooleanField(default=False)
    is_vegetarian = models.BooleanField(default=False)

    def __str__(self):
        return self.name
