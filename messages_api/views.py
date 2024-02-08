from rest_framework import status ,generics ,permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import MyTokenObtainPairSerializer, UserSerializer , MessageSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Q
from .models import Message

class CreateMessageView(generics.CreateAPIView):
    """
    API view to create a new message. Only authenticated users can create messages.
    The sender is automatically set to the current authenticated user.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Set the sender of the message to the current user before saving.
        serializer.save(sender=self.request.user)

class ListUserMessagesView(generics.ListAPIView):
    """
    API view to list all messages where the current user is either the sender or the receiver.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Fetch messages where the current user is either the sender or receiver.
        user = self.request.user
        return Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)

class ListUnreadMessagesView(generics.ListAPIView):
    """
    API view to list all unread messages for the current user.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Fetch unread messages where the current user is the receiver.
        user = self.request.user
        return Message.objects.filter(receiver=user, is_read=False)

class MessageDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve details of a specific message. Marks the message as read if the current user is the receiver.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Mark the message as read if the current user is the receiver.
        if instance.receiver == request.user:
            instance.is_read = True
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class MessageDeleteView(generics.DestroyAPIView):
    """
    API view to delete a specific message. Both the sender and receiver have the permission to delete the message.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Allow deletion of a message if the current user is either the sender or the receiver.
        user = self.request.user
        return Message.objects.filter(Q(sender=user) | Q(receiver=user))

class UserCreate(APIView):
    """
    API view for user registration. Allows new users to create an account.
    """
    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                # Return the user data upon successful registration.
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Return validation errors if the user data is invalid.    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyTokenObtainPairView(TokenObtainPairView):
    """
    Custom TokenObtainPairView that uses a modified serializer to include additional information in the JWT response.
    """
    serializer_class = MyTokenObtainPairSerializer