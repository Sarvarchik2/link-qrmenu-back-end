from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantAdminViewSet, RestaurantOwnerInfoView, CategoryViewSet, MenuItemViewSet, RestaurantMenuView, RestaurantOrderCreateView

router = DefaultRouter()
router.register(r'admin/restaurants', RestaurantAdminViewSet, basename='admin-restaurants')

owner_router = DefaultRouter()
owner_router.register(r'owner/categories', CategoryViewSet, basename='owner-categories')
owner_router.register(r'owner/items', MenuItemViewSet, basename='owner-items')

urlpatterns = [
    path('', include(router.urls)),
    path('owner/info/', RestaurantOwnerInfoView.as_view(), name='owner-info'),
    path('<slug:restaurant_slug>/menu/', RestaurantMenuView.as_view(), name='restaurant-menu'),
    path('<slug:restaurant_slug>/order/', RestaurantOrderCreateView.as_view(), name='restaurant-order'),
]
urlpatterns += owner_router.urls 