from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from status.models import Status


class StatusTestCase(APITestCase):
    def test_get_status_by_authenticated_use(self):
        url = reverse('last-message-api')
        # data = Status.objects.get_latest_messages()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
