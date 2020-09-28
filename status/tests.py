from django.test import TestCase, RequestFactory
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse, reverse_lazy
from status.models import Status
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class UpdatePost(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user('testuser', 'testuser@mail.com', 'testuser')
        self.client.login(username='testuser', password='testuser')
        self.user = User.objects.create_user('testuser1', 'testuser1@mail.com', 'testuser1')

    def test_can_update_status_by_owner(self, *args, **kwargs):
        qs  = Status.objects.create(message="hello", user=self.owner)
        payload = {'message': 'message updated', 'user':self.owner}
        url = reverse('status:update-list', kwargs={'pk': qs.pk})
        response = self.client.put(url , payload)
        print(response)
        self.assertEqual(str(qs.user), str(self.user))
        self.assertEqual(response.status_code,status.HTTP_200_OK )

    def test_delete_status_by_owner(self):
        pass


class StatusTestCase(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'testuser', 'testuser@mail.com', 'testpassword')
        self.client.login(username='testuser', password='testpassword')
        # self.user = User.objects.create(username="mike")

    def test_get_status_by_authenticated_use(self):
        url = reverse('last-message-api')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
