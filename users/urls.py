from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserDetailsView

urlpatterns = [
    # Registration
    path('register/', RegisterView.as_view(), name='register'),

    # JWT login and refresh
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Authenticated user detail & partial update
    path('me/', UserDetailsView.as_view(), name='user_details'),

]
