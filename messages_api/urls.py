from django.urls import path
from .views import CreateMessageView, ListUnreadMessagesView, ListUserMessagesView, MessageDeleteView, MessageDetailView, UserCreate

urlpatterns = [
    path('register/', UserCreate.as_view(), name='register'),
    path('messages/', CreateMessageView.as_view(), name='create_message'),
    path('messages/all/', ListUserMessagesView.as_view(), name='list_messages'),
    path('messages/unread/', ListUnreadMessagesView.as_view(), name='list_unread_messages'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='delete_message'),
]
