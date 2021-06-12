from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from accounts.models import CustomUser

import json


class TestLoginCase(APITestCase):
    login_url = reverse('rest_login')

    email = 'test@user.com'
    password = 'kah2ie3urh4k'
    nickname = 'test1'
    gender = 'M'

    not_registered_email = "emptydb@emptydb.com"
    not_matched_password = 'random!'

    def setUp(self):
        self.user = CustomUser.objects.create_user(self.email, self.password, self.nickname, self.gender)

    def test_login_success(self): 
        data = {
            'email': self.email, 'password': self.password
        }
        r = self.client.post(self.login_url, json.dumps(data), content_type="application/json")
        body = r.content
        res_json = r.json()
        self.assertEqual(r.status_code, status.HTTP_200_OK, body)
        self.assertEqual(self.user.email, res_json['user']['email'])

    def test_login_fail_response_415(self):
        data = {
            'email': self.email, 'password': self.password
        }
        r = self.client.post(self.login_url, data)
        body = r.content
        self.assertEqual(r.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, body)

    def test_login_fail_email_is_empty(self):
        data = {
            'email': self.email
        }
        r = self.client.post(self.login_url, json.dumps(data), content_type="application/json")
        body = r.content
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST, body)

    def test_login_fail_password_is_empty(self):
        data = {
            'password': self.password
        }
        r = self.client.post(self.login_url, json.dumps(data), content_type="application/json")
        body = r.content
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST, body)

    def test_login_fail_email_does_not_exist_in_db(self):
        data = {
            'email': self.not_registered_email
        }
        r = self.client.post(self.login_url, json.dumps(data), content_type="application/json")
        body = r.content
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST, body)

    def test_login_fail_wrong_password(self):
        data = {
            'email': self.email,
            'password': self.not_matched_password
        }
        r = self.client.post(self.login_url, json.dumps(data), content_type="application/json")
        body = r.content
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST, body)

    def test_login_fail_not_allowed_method(self):
        data = {
            'email': self.email,
            'password': self.not_matched_password
        }
        r = self.client.put(self.login_url, json.dumps(data), content_type="application/json")
        body = r.content
        self.assertEquals(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, body)