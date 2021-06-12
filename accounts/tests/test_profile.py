from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from accounts.models import CustomUser

import json


class TestProfileCase(APITestCase):
    profile_url = reverse('rest_profile')
    login_url = reverse('rest_login')

    email = 'test@user.com'
    password = 'kah2ie3urh4k'
    nickname = 'test1'
    gender = 'M'

    new_gender = 'F'

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
    
    def test_put_success(self):
        _, body = self._login()
        req = {
            'email': body['user']['email'],
            'gender': self.new_gender,
        }
        r = self.client.put(self.profile_url, json.dumps(req), content_type="application/json")
        body = r.content
        self.assertEquals(r.status_code, status.HTTP_204_NO_CONTENT, body)

    def test_get_success(self):
        _, body = self._login()
        r = self.client.get(self.profile_url, content_type="application/json")
        body = r.content
        body_json = r.json()
        self.assertEquals(r.status_code, status.HTTP_200_OK, body)
        self.assertEquals(self.email, body_json.get('email'))
        self.assertEquals(self.nickname, body_json.get('nickname'))
        self.assertEquals(self.gender, body_json.get('gender'))
        self.assertFalse(body_json.get('is_subscribed'))

