from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from users.views import PointRetrieveUpdateView

User = get_user_model()


class TestPoints(TestCase):
    factory = APIRequestFactory()
    view = PointRetrieveUpdateView.as_view()

    def setUp(self) -> None:
        user = User.objects.create(username="test_user", is_superuser=True, is_staff=True)
        user.set_password("test_password")
        user.save()

        User.objects.create(username="user_with_points", points=50000)

        self.client.login(username="test_user", password="test_password")

    def test_get_points(self):
        response = self.client.get('/api/v1/users/1/points/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual({'points': 0}, response.json())

        self.client.logout()
        response = self.client.get('/api/v1/users/1/points/')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_add_points(self):
        response = self.client.patch('/api/v1/users/1/points/',
                                     data={"points_added": 50000},
                                     content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual({"points": 50000}, response.json())

        response = self.client.get('/api/v1/users/1/points/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual({'points': 50000}, response.json())

        self.client.logout()

        response = self.client.patch('/api/v1/users/1/points/',
                                     data={"points_added": 50000},
                                     content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_spend_points(self):
        user = User.objects.get(username="user_with_points")
        response = self.client.patch(f'/api/v1/users/{user.id}/points/',
                                     data={"points_spent": 5000},
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual({"points": 45000}, response.json())

        response = self.client.get(f'/api/v1/users/{user.id}/points/')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual({"points": 45000}, response.json())

        self.client.logout()

        response = self.client.patch(f'/api/v1/users/{user.id}/points/',
                                     data={"points_spent": 5000},
                                     content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_not_enough_points(self):
        user = User.objects.get(username="user_with_points")
        response = self.client.get(f'/api/v1/users/{user.id}/points/')

        original_points = response.json()['points']

        response = self.client.patch(f'/api/v1/users/{user.id}/points/',
                                     data={"points_spent": original_points + 1000},
                                     content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual({"points": "Not enough points."}, response.json())
