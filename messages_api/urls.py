from django.urls import path
from .views import (
    CreateMessageView, 
    ListUnreadMessagesView, 
    ListUserMessagesView, 
    MessageDeleteView, 
    MessageDetailView, 
    UserCreate
)

urlpatterns = [
    # User registration endpoint
    path('register/', UserCreate.as_view(), name='register'),

    # Endpoint to create a new message
    path('messages/', CreateMessageView.as_view(), name='create_message'),

    # Endpoint to list all messages where the user is either sender or receiver
    path('messages/all/', ListUserMessagesView.as_view(), name='list_messages'),

    # Endpoint to list all unread messages for the current user
    path('messages/unread/', ListUnreadMessagesView.as_view(), name='list_unread_messages'),

    # Endpoint to get details of a specific message and mark it as read
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),

    # Endpoint to delete a specific message (as sender or receiver)
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='delete_message'),
]
