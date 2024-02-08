from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Message

class UserRegistrationAndAuthenticationTests(APITestCase):
    def setUp(self):
        """
        Perform initializations (like user registration) before each test method.
        """
        self.user_registration_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        }
        self.register_url = reverse('register')
        self.token_url = reverse('token_obtain_pair')

    def test_user_registration(self):
        """
        Ensure we can create a new user.
        """
        response = self.client.post(self.register_url, self.user_registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('id' in response.data)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_obtain_jwt_token(self):
        """
        Ensure we can obtain a JWT token for a registered user.
        """
        # Register a user
        self.client.post(self.register_url, self.user_registration_data, format='json')
        data = {'username': 'testuser', 'password': 'password123'}
        response = self.client.post(self.token_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)

class MessageTests(APITestCase):
    def setUp(self):
            """
            Create two users and authenticate one for the test cases.
            """
            # Create two users
            self.user1 = User.objects.create_user(username='user1', password='testpassword1')
            self.user2 = User.objects.create_user(username='user2', password='testpassword2')


    def get_token_for_user(self, username, password):
        """
        Obtain JWT token for a given user.
        """
        response = self.client.post(reverse('token_obtain_pair'), {'username': username, 'password': password}, format='json')
        return response.data['access']
    
    def authenticate(self, username, password):
        """
        Authenticate a user for subsequent requests.
        """
        token = self.get_token_for_user(username, password)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_create_message(self):
        """
        Ensure we can create a new message from one user to another.
        """
        self.authenticate('user1', 'testpassword1') 
        url = reverse('create_message')
        data = {
            'receiver_username': 'user2',
            'message': 'Hello from user1',
            'subject': 'Greeting'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Message.objects.filter(sender=self.user1, receiver=self.user2).exists())

    def test_list_user_messages(self):
        """
        Ensure a user can list all messages where they are the sender or receiver.
        """
        # Need to create a message first for there to be something to list
        self.test_create_message()
        self.authenticate('user2', 'testpassword2')  # Switch authentication to user2
        url = reverse('list_messages')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Expecting one message

    def test_list_unread_messages(self):
        """
        Ensure a user can list all unread messages they have received.
        """
        # Create a message first to ensure there's an unread message to list
        self.test_create_message()
        self.authenticate('user2', 'testpassword2')  # Switch authentication to user2
        url = reverse('list_unread_messages')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Expecting one unread message

    def test_read_message_detail(self):
        """
        Ensure a user can read a specific message detail.
        """
        # Create a message first
        self.test_create_message()
        message = Message.objects.get(sender=self.user1, receiver=self.user2)
        self.authenticate('user2', 'testpassword2')  # Authenticate as user2 to read the message
        url = reverse('message_detail', kwargs={'pk': message.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Hello from user1')

    def test_delete_message(self):
        """
        Ensure a user can delete a message they sent or received.
        """
        # Create a message first
        self.test_create_message()
        message = Message.objects.get(sender=self.user1, receiver=self.user2)
        self.authenticate('user1', 'testpassword1')  # Authenticate as user1 to delete the message
        url = reverse('delete_message', kwargs={'pk': message.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Message.objects.filter(id=message.id).exists())
