from functools import partial
from datetime import timedelta
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
import unittest.mock as mock
import json

from accounts.models import CustomUser
from utils.time import *


class TestLogOutCase(APITestCase):

    login_url = reverse('rest_login')
    profile_url = reverse('rest_profile')
    logout_url = reverse('rest_logout')

    email = 'test@user.com'
    password = 'kah2ie3urh4k'
    nickname = 'test1'
    gender = 'M'
    

    def setUp(self):
        self.user = CustomUser.objects.create_user(self.email, self.password, self.nickname, self.gender, self.grade)

    def _login(self):
        data = {
            'email': self.email, 'password': self.password
        }
        r = self.client.post(self.login_url, json.dumps(data), content_type="application/json")
        body = r.json()
        if 'access_token' in body:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer %s' % body['access_token'])
        return r.status_code, body

    def test_logout_response_200(self):
        _, body = self._login()
        req = {'refresh': body['refresh_token']}
        r = self.client.post(self.logout_url, json.dumps(req), content_type="application/json")
        body = r.content
        self.assertEquals(r.status_code, status.HTTP_200_OK, body)
        self.assertTrue(body, body)

    def test_logout_fail_response_415(self):
        _, body = self._login()
        data = {'refresh': body['refresh_token']}
        r = self.client.post(self.logout_url, data)
        body = r.content
        self.assertEquals(r.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, body)

    def test_logout_with_bad_refresh_token_response_401(self):
        self._login()
        req = {'refresh': 'dsf.sdfsdf.sdf'}
        r = self.client.post(self.logout_url, json.dumps(req), content_type="application/json")
        body = r.json()
        self.assertEquals(r.status_code, status.HTTP_401_UNAUTHORIZED, body)
        self.assertTrue(body, body)

    def test_logout_refresh_token_in_blacklist(self):
        _, body = self._login()
        req = {'refresh': body['refresh_token']}
        r = self.client.post(self.logout_url, json.dumps(req), content_type="application/json")
        token = partial(RefreshToken, body['refresh_token'])
        self.assertRaises(TokenError, token)

    def test_access_token_still_valid_after_logout(self):
        _, body = self._login()
        req = {'refresh': body['refresh_token']}
        self.client.post(self.logout_url, json.dumps(req), content_type="application/json")
        r = self.client.get(self.profile_url)
        body = r.json()
        self.assertEquals(r.status_code, status.HTTP_200_OK, body)
        self.assertTrue(body, body)

    def test_access_token_invalid_in_2_hour_after_logout(self):
        _, body = self._login()
        req = {'refresh': body['refresh_token']}
        self.client.post(self.logout_url, req)
        m = mock.Mock()
        m.return_value = aware_utc_now() + timedelta(hours=2)
        with mock.patch('rest_framework_simplejwt.tokens.aware_utcnow', m):
            r = self.client.get(self.profile_url)
            body = r.json()
        self.assertEquals(r.status_code, status.HTTP_401_UNAUTHORIZED, body)
        self.assertTrue(body, body)

    def test_other_method_not_allowed(self):
        _, body = self._login()
        req = {'refresh': body['refresh_token']}
        r = self.client.put(self.logout_url, req)
        body = r.content
        self.assertEquals(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, body)