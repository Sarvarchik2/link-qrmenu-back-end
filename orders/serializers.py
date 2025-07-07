from rest_framework import serializers
from .models import Order, OrderItem
from restaurants.serializers import MenuItemSerializer
from restaurants.models import MenuItem

class OrderItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для позиции заказа.
    Пример:
    {
        "id": 1,
        "menu_item": {"id": 1, "name": "Капучино"},
        "menu_item_id": 1,
        "quantity": 2
    }
    """
    menu_item = MenuItemSerializer(read_only=True)
    menu_item_id = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all(), source='menu_item', write_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_id', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для заказа.
    Пример:
    {
        "id": 1,
        "restaurant": 1,
        "guest_name": "Иван",
        "table_number": "5",
        "status": "new",
        "created_at": "2024-07-01T12:00:00Z",
        "items": [
            {"menu_item_id": 1, "quantity": 2}
        ]
    }
    """
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'restaurant', 'guest_name', 'table_number', 'status', 'created_at', 'items'] 