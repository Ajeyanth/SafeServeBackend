from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.contrib.auth import get_user_model

from restaurants.models import MenuItem
from restaurants.serializers import MenuItemSerializer
from .serializers import UserSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """
    Allows anyone to register a new user (customer or owner).
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserDetailsView(APIView):
    """
    GET: Returns the current user's info (must be authenticated).
    PATCH: Updates the user's dietary_restrictions (or other fields).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,  # e.g., 'customer' or 'owner'
            "dietary_restrictions": user.dietary_restrictions,
        })

    def patch(self, request):
        user = request.user
        # Example: the user can update dietary_restrictions via PATCH
        new_dietary = request.data.get('dietary_restrictions', '')
        user.dietary_restrictions = new_dietary
        user.save()

        return Response({
            "detail": "Dietary restrictions updated successfully.",
            "dietary_restrictions": user.dietary_restrictions,
        })
