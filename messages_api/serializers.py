from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Message
from django.core.exceptions import ObjectDoesNotExist

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user_id'] = user.id
        # You can add more custom claims here

        return token

class MessageSerializer(serializers.ModelSerializer):
    receiver_username = serializers.CharField(write_only=True, required=True)  # For client input

    class Meta:
        model = Message
        fields = ['id', 'sender', 'message', 'subject', 'creation_date', 'is_read', 'receiver_username']
        read_only_fields = ('id', 'sender', 'creation_date', 'is_read')

    def create(self, validated_data):
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
        representation = super().to_representation(instance)
        # Add the receiver's username to the output for clarity
        representation['receiver_username'] = instance.receiver.username
        return representation