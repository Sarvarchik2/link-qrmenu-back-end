from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Restaurant
from .serializers import RestaurantSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.exceptions import NotFound

# Create your views here.

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'superadmin'

class RestaurantAdminViewSet(viewsets.ModelViewSet):
    """Управление ресторанами (GET, POST /api/admin/restaurants/) — только для администратора."""
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsSuperAdmin]

    @swagger_auto_schema(
        operation_description="Получить список всех ресторанов.",
        tags=["Администратор"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать новый ресторан и владельца.",
        tags=["Администратор"]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'owner'

    def has_object_permission(self, request, view, obj):
        # Для Restaurant
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        # Для Category
        if hasattr(obj, 'restaurant'):
            return obj.restaurant == request.user.restaurant
        # Для MenuItem
        if hasattr(obj, 'category') and hasattr(obj.category, 'restaurant'):
            return obj.category.restaurant == request.user.restaurant
        return False

from rest_framework import generics
from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer

class RestaurantOwnerInfoView(generics.RetrieveUpdateAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [IsOwner]

    def get_object(self):
        return self.request.user.restaurant

from rest_framework import viewsets

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'restaurant'):
            return Category.objects.filter(restaurant=user.restaurant)
        return Category.objects.none()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsOwner()]

    def perform_create(self, serializer):
        serializer.save(restaurant=self.request.user.restaurant)

class MenuItemViewSet(viewsets.ModelViewSet):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'restaurant'):
            # Только блюда ресторана владельца
            return MenuItem.objects.filter(category__restaurant=user.restaurant)
        # Для анонимных пользователей (например, Swagger) — пустой queryset
        return MenuItem.objects.none()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsOwner()]

    def perform_create(self, serializer):
        serializer.save()

from rest_framework.response import Response
from rest_framework import status
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer

class RestaurantMenuView(generics.RetrieveAPIView):
    """Публичное меню ресторана для гостей (GET /api/{restaurant_slug}/menu/)."""
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'restaurant_slug'
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Получить меню ресторана (категории и блюда) по slug.",
        responses={200: openapi.Response('Меню', CategorySerializer(many=True))},
        tags=["Гость"]
    )
    def get(self, request, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(slug=kwargs['restaurant_slug'])
        except Restaurant.DoesNotExist:
            raise NotFound("Ресторан не найден")
        categories = Category.objects.filter(restaurant=restaurant, parent=None)
        data = CategorySerializer(categories, many=True).data
        restaurant_data = RestaurantSerializer(restaurant).data
        return Response({
            'restaurant': restaurant_data,
            'categories': data
        })

class RestaurantOrderCreateView(generics.CreateAPIView):
    """Оформление заказа гостем (POST /api/{restaurant_slug}/order/)."""
    serializer_class = OrderSerializer
    lookup_url_kwarg = 'restaurant_slug'
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Оформить заказ в ресторане по slug.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["guest_name", "table_number", "items"],
            properties={
                'guest_name': openapi.Schema(type=openapi.TYPE_STRING, description='Имя гостя'),
                'table_number': openapi.Schema(type=openapi.TYPE_STRING, description='Номер столика или "навынос"'),
                'items': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'menu_item_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID блюда'),
                            'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Количество'),
                        }
                    ),
                ),
            },
        ),
        responses={201: openapi.Response('Заказ создан', OrderSerializer)},
        tags=["Гость"]
    )
    def create(self, request, *args, **kwargs):
        restaurant = Restaurant.objects.get(slug=kwargs['restaurant_slug'])
        guest_name = request.data.get('guest_name')
        table_number = request.data.get('table_number')
        items = request.data.get('items', [])
        order = Order.objects.create(restaurant=restaurant, guest_name=guest_name, table_number=table_number)
        for item in items:
            OrderItem.objects.create(order=order, menu_item_id=item['menu_item_id'], quantity=item['quantity'])
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
