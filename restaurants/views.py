from rest_framework import generics, status
from rest_framework.response import Response
from django.db import transaction
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from users.serializers import UserSerializer  # For owner registration
from .models import Restaurant, MenuItem, Category
from .serializers import RestaurantSerializer, MenuItemSerializer, CategorySerializer
import qrcode
from io import BytesIO
from django.http import HttpResponse
from rest_framework.views import APIView

class RestaurantListCreateView(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RestaurantDetailView(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class MenuItemListCreateView(generics.ListCreateAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        return MenuItem.objects.filter(restaurant_id=restaurant_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        restaurant_id = self.kwargs['restaurant_id']
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id, owner=self.request.user)
            context['restaurant'] = restaurant
        except Restaurant.DoesNotExist:
            context['restaurant'] = None
        return context

    def perform_create(self, serializer):
        restaurant_id = self.kwargs['restaurant_id']
        restaurant = Restaurant.objects.get(pk=restaurant_id, owner=self.request.user)
        serializer.save(restaurant=restaurant)



class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        return Category.objects.filter(restaurant_id=restaurant_id)

    def perform_create(self, serializer):
        restaurant_id = self.kwargs['restaurant_id']
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id, owner=self.request.user)
            serializer.save(restaurant=restaurant)
        except Exception as e:
            print("DEBUG: Error in perform_create (CategoryListCreateView):", e)
            raise e


class RegisterOwnerView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(role='owner')
        Restaurant.objects.create(
            owner=user,
            name=f"{user.username}'s Restaurant",
            location="Default Location",
            cuisine_type="General"
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GenerateQRCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, restaurant_id):
        try:
            # Optionally enforce ownership:
            # restaurant = Restaurant.objects.get(id=restaurant_id, owner=request.user)
            menu_url = f"http://192.168.1.111:3000/restaurant/{restaurant_id}/menu"
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(menu_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            return HttpResponse(buffer, content_type="image/png")
        except Restaurant.DoesNotExist:
            return Response({"error": "Restaurant not found or not owned by you."}, status=status.HTTP_404_NOT_FOUND)
