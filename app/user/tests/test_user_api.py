from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    '''Tests the users API (public)'''

    def setUp(self):
        '''will be started before every test (cleaner code)'''
        self.client = APIClient()  # test client for our tests

    def test_create_valid_user_success(self):
        '''Test creating user width valid payload is successful'''
        payload = {
            'email': 'test1@drawnet.pl',
            'password': 'testpass',
            'name': 'TestUser'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)  # asks for user to check if created
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)  # in this way we avoid to send pass

    def test_user_exists(self):
        '''Test creating user that already exists fails'''
        payload = {
                    'email': 'test1@drawnet.pl',
                    'password': 'testpass'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        '''Test that the password must be more than 7 characters'''
        payload = {
            'email': 'test1@drawnet.pl',
            'password': 'pw1234',  # length == 6
            'name': 'TestUser'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        '''Test that a token is created for the user'''
        payload = {
        'email': 'test1@drawnet.pl',
        'password': 'testpass'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        '''Test if token is not created if invalid credentials are given'''
        create_user(email = 'test1@drawnet.pl', password = 'testpass')
        payload = {
        'email': 'test1@drawnet.pl',
        'password': 'wrong_pass'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        '''Test that token is not created if user doesn't exist'''
        payload = {'email': 'test1@drawnet.pl', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        '''Test that e-mail and password are required'''
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)