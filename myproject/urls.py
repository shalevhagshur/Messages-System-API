from django.contrib import admin
from django.urls import path, include
from messages_api.views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # Django admin interface
    path('admin/', admin.site.urls),
    
    # Include all URLs from the messages_api app
    # This allows for separation of concerns and better modularity by keeping app-specific URLs in their respective urls.py files
    path('api/', include('messages_api.urls')), 
    
    # Custom JWT token obtain endpoint
    # This endpoint uses a customized view to handle token creation, possibly including additional claims or custom validation
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # JWT token refresh endpoint
    # Allows clients to obtain a new access token using a valid refresh token without requiring username and password again
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # JWT token verification endpoint
    # Clients can use this endpoint to verify the validity of their access token
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
