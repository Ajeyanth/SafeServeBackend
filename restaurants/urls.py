from django.urls import path
from .views import (
    RestaurantListCreateView,
    MenuItemListCreateView,
    RegisterOwnerView,
    RestaurantDetailView,
    GenerateQRCodeView,
    CategoryListCreateView, MenuItemDetailView,
)

urlpatterns = [
    path('', RestaurantListCreateView.as_view(), name='restaurant_list_create'),

    path('<int:pk>/', RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('<int:restaurant_id>/menu/', MenuItemListCreateView.as_view(), name='menu_item_list_create'),
    path('register-owner/', RegisterOwnerView.as_view(), name='register_owner'),
    path('<int:restaurant_id>/generate-qr/', GenerateQRCodeView.as_view(), name='generate_qr'),
    path('<int:restaurant_id>/categories/', CategoryListCreateView.as_view(), name='category_list_create'),
    path('<int:restaurant_id>/menu/<int:pk>/', MenuItemDetailView.as_view(), name='menu_item_detail'),

]
