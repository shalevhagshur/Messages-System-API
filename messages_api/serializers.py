from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Message

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for Django's User model.
    Used for user registration with write-only password field to ensure password confidentiality.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Overridden create method to use Django's create_user method,
        ensuring the password is properly hashed.
        """
        user = User.objects.create_user(**validated_data)
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom TokenObtainPairSerializer to add additional claims to the JWT token.
    """
    @classmethod
    def get_token(cls, user):
        """
        Adds custom claims to the JWT token. Here, user_id is added for identifying the user.
        """
        token = super().get_token(user)
        # Custom claims
        token['user_id'] = user.id
        return token

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model, including a write-only field for receiver_username
    to simplify message sending.
    """
    receiver_username = serializers.CharField(write_only=True, required=True)  # For client input

    class Meta:
        model = Message
        fields = ['id', 'sender', 'message', 'subject', 'creation_date', 'is_read', 'receiver_username']
        read_only_fields = ('id', 'sender', 'creation_date', 'is_read')

    def create(self, validated_data):
        """
        Overridden create method to handle message creation with receiver identified by username.
        Raises ValidationError if receiver username does not exist.
        """
        receiver_username = validated_data.pop('receiver_username')
        try:
            receiver = User.objects.get(username=receiver_username)  # Attempt to get the receiver user object
        except User.DoesNotExist:
            # If no user is found with the provided username, raise a validation error
            raise serializers.ValidationError({"receiver_username": "No user found with this username"})
        
        validated_data['receiver'] = receiver
        validated_data['sender'] = self.context['request'].user  # Set sender from request
        message = super().create(validated_data)
        return message

    def to_representation(self, instance):
        """
        Modify the default representation to include receiver_username in the response.
        """
        representation = super().to_representation(instance)
        # Add the receiver's username to the output for clarity
        representation['receiver_username'] = instance.receiver.username
        return representation