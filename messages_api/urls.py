from django.urls import path
from .views import UserCreate, SendMessageView, UserMessagesView

urlpatterns = [
    path('register/', UserCreate.as_view(), name='register'),
    path('send/', SendMessageView.as_view(), name='send_message'),
    path('messages/', UserMessagesView.as_view(), name='user_messages'),
]
