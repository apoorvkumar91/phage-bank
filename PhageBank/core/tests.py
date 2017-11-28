from django.test import TestCase
import unittest,os,shutil
from django.test import Client
from django.contrib.auth.models import User

class SimpleTest(TestCase):    #unittest.TestCase
    valid_credentials = {
        'username': "test_user",
        'password': 'pass@123'}
    invalid_credentials = {
        'username': 'abcde',
        'password': '12345'}

    #client = Client()

    def setUp(self):
        # Every test needs a client.
        user = User.objects.create_user("test_user", 'testuser@test.com', 'pass@123')
        user.save()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get('/mylogin/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_user_exist(self):
        # Check that login is successful with valid user
        response = self.client.post('/mylogin/', self.valid_credentials, follow=True)
        #self.assertEqual(response.status_code,200)
        
        form_is_valid = response.json()['form_is_valid']
        self.assertEqual(form_is_valid,True)

    def test_user_doesnt_exist(self):
        # Check that login is unsuccessful with invalid user
        response = self.client.post('/mylogin/', self.invalid_credentials, follow=True)
        #index = response.content.find(b"Your username and password didn\'t match. Please try again.")
        
        form_is_valid = response.json()['form_is_valid']
        
        self.assertEqual(form_is_valid,False)
# Create your tests here.

    def test_add_phage_ut(self):
        phage_desc = {"phage_name" : "test_newphage", "phage_CPT_id" : "test_123", "phage_lab": "Lab-A", "flag":1}
        self.client.login(username = "test_user", password= 'pass@123')
        response = self.client.post('/add_phage/', phage_desc, follow=True)
        
        approvePhage = response.json()['approvePhage']
        approveCPTid = response.json()['approveCPTid']
        
        self.assertEqual(approvePhage,1)
        self.assertEqual(approveCPTid,1)
        
        
        























