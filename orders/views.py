from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from .models import Order
from .serializers import OrderSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'owner'

    def has_object_permission(self, request, view, obj):
        return obj.restaurant == request.user.restaurant

class OrderOwnerViewSet(viewsets.ModelViewSet):
    """Управление заказами владельцем ресторана (GET, PUT/PATCH /api/owner/orders/)."""
    serializer_class = OrderSerializer
    permission_classes = [IsOwner]
    filter_backends = [filters.SearchFilter]
    search_fields = ['status']

    def get_queryset(self):
        return Order.objects.filter(restaurant=self.request.user.restaurant)

    def perform_update(self, serializer):
        serializer.save()

    @swagger_auto_schema(
        operation_description="Получить список заказов для ресторана владельца. Фильтрация по статусу.",
        tags=["Владелец"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Изменить статус заказа (например, отметить как выполненный).",
        tags=["Владелец"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
