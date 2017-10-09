from django.test import TestCase
import unittest
from django.test import Client
from django.contrib.auth.models import User

class SimpleTest(unittest.TestCase):
    user = User.objects.create(username='testuser', password='pass@123', email='testuser@test.com')
    user.save()
    valid_credentials = {
        'username': 'testuser',
        'password': 'pass@123'}
    invalid_credentials = {
        'username': 'abcde',
        'password': '12345'}
    client = Client()

    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get('/login/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_user_exist(self):
        # Check that login is successful with valid user
        response = self.client.post('/login/', self.valid_credentials, follow=True)
        self.assertEqual(response.status_code,200)

    def test_user_doesnt_exist(self):
        # Check that login is unsuccessful with invalid user
        response = self.client.post('/login/', self.invalid_credentials, follow=True)
        index = response.content.find("Your username and password didn't match. Please try again.")
        self.assertNotEqual(index,-1)
# Create your tests here.
