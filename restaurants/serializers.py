from rest_framework import serializers
from .models import Restaurant, Category, MenuItem

class RestaurantSerializer(serializers.ModelSerializer):
    """
    Сериализатор для ресторана.
    Пример:
    {
        "id": 1,
        "owner": 2,
        "name": "Ресторан Пример",
        "description": "Лучший ресторан города!",
        "contacts": "+7 999 123-45-67",
        "address": "г. Москва, ул. Пример, 1",
        "logo": "/media/logos/logo.png",
        "slug": "primer-restaurant"
    }
    """
    class Meta:
        model = Restaurant
        fields = ['id', 'owner', 'name', 'description', 'contacts', 'address', 'logo', 'slug']

class MenuItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для блюда.
    Пример:
    {
        "id": 1,
        "category": 1,
        "name": "Капучино",
        "description": "Кофе с молоком и пенкой",
        "price": "250.00",
        "photo": "/media/menu_items/cappuccino.png",
        "is_hit": true,
        "is_vegetarian": false
    }
    """
    class Meta:
        model = MenuItem
        fields = ['id', 'category', 'name', 'description', 'price', 'photo', 'is_hit', 'is_vegetarian']

class CategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)

    """
    Сериализатор для категории меню.
    Пример:
    {
        "id": 1,
        "restaurant": 1,
        "parent": null,
        "name": "Напитки"
    }
    """
    class Meta:
        model = Category
        fields = ['id', 'restaurant', 'parent', 'name', 'photo', 'items'] 