from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderOwnerViewSet

router = DefaultRouter()
router.register(r'owner/orders', OrderOwnerViewSet, basename='owner-orders')

urlpatterns = [
    path('', include(router.urls)),
] 