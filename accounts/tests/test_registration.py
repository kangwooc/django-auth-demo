from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from accounts.models import CustomUser

import json

class TestRegistrationCase(APITestCase):
    signup_url = reverse('rest_signup')
    login_url = reverse('rest_login')

    email = 'test@user.com'
    password = 'kah2ie3urh4k'
    nickname = 'test1'
    gender = 'M'

    invalid_email = 'test1.adfcom'
    invalid_password = 'cf'
    invalid_gender_input = 'randominput'
    
    random_password = 'asdfasddf'

    def _login(self, email, password):
        data = {
            'email': email, 'password': password
        }
        r = self.client.post(self.login_url, json.dumps(data), content_type="application/json")
        body = r.json()
        if 'access_token' in body:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer %s' % body['access_token'])
        return r.status_code, body

    def test_signup_success(self):
        data = {
            'email': self.email,
            'password1': self.password,
            'password2': self.password,
            'nickname': self.nickname,
            'gender': self.gender
        }
        r = self.client.post(self.signup_url, json.dumps(data), content_type="application/json")
        body = r.content
        res_json = r.json()
        self.assertEqual(r.status_code, status.HTTP_201_CREATED, body)
        self.assertEqual(data['email'], res_json['user']['email'])
        status_code, body = self._login(res_json['user']['email'], self.password)
        self.assertEqual(status_code, status.HTTP_200_OK)
        
    def test_signup_fail_response_415(self):
        data = {
            'email': self.email,
            'password': self.password,
            'nickname': self.nickname,
            'gender': self.gender,
        }
        r = self.client.post(self.login_url, data)
        body = r.content
        self.assertEqual(r.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, body)

    def test_signup_fail_input_different_password(self):
        data = {
            'email': self.email,
            'password1': self.random_password,
            'password2': self.password,
            'nickname': self.nickname,
            'gender': self.gender
        }
        r = self.client.post(self.signup_url, json.dumps(data), content_type="application/json")
        body = r.content
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST, body)

    def test_signup_fail_invalid_password(self):
        data = {
            'email': self.email,
            'password1': self.invalid_password,
            'password2': self.invalid_password,
            'nickname': self.nickname,
            'gender': self.gender
        }
        r = self.client.post(self.signup_url, json.dumps(data), content_type="application/json")
        body = r.content
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST, body)

    def test_signup_fail_invalid_option_for_gender(self):
        data = {
            'email': self.email,
            'password1': self.invalid_password,
            'password2': self.invalid_password,
            'nickname': self.nickname,
            'gender': self.invalid_gender_input
        }
        r = self.client.post(self.signup_url, json.dumps(data), content_type="application/json")
        body = r.content
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST, body)


    def test_signup_fail_invalid_option_for_eng_level(self):
        data = {
            'email': self.email,
            'password1': self.invalid_password,
            'password2': self.invalid_password,
            'nickname': self.nickname,
            'gender': self.gender
        }
        r = self.client.post(self.signup_url, json.dumps(data), content_type="application/json")
        body = r.content
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST, body)

    def test_signup_fail_other_methods_not_allowed(self):
        data = {
            'email': self.email,
            'password1': self.invalid_password,
            'password2': self.invalid_password,
            'nickname': self.nickname,
            'gender': self.gender
        }
        r = self.client.put(self.signup_url, json.dumps(data), content_type="application/json")
        body = r.content
        self.assertEquals(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, body)
