from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from users.views import PointRetrieveUpdateView


__all__ = [
    "TestPoints"
]

User = get_user_model()


class TestPoints(TestCase):
    factory = None
    test_view = None

    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.test_view = PointRetrieveUpdateView.as_view()

        User.objects.create(id=1, username="admin_user", is_superuser=True, is_staff=True)
        User.objects.create(id=2, username="user_with_points", points=50000)
        User.objects.create(id=3, username="user_with_no_points")

    def test_get_points(self):
        # Get points with Admin User.
        user = User.objects.get(pk=1)
        request = self.factory.get('api/v1/users/1/points/')
        force_authenticate(request, user)
        response = self.test_view(request, pk=user.pk)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual({'points': 0}, response.data)

        # Get points with no authentication.
        request = self.factory.get('api/v1/users/1/points/')
        response = self.test_view(request, pk=1)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        # Get points with non admin user.
        user = User.objects.get(pk=3)
        request = self.factory.get('api/v1/users/1/points/')
        force_authenticate(request, user)
        response = self.test_view(request, pk=1)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_add_points(self):
        # Add points with admin user.
        user = User.objects.get(pk=1)
        request = self.factory.patch('/api/v1/users/1/points/', {"points_added": 50000}, format='json')
        force_authenticate(request, user)
        response = self.test_view(request, pk=user.pk)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual({"points": 50000}, response.data)

        # Check updated points.
        request = self.factory.get('/api/v1/users/1/points/')
        force_authenticate(request, user)
        response = self.test_view(request, pk=user.pk)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual({'points': 50000}, response.data)

        # Add points with no authentication.
        request = self.factory.patch('/api/v1/users/1/points/',
                                     data={"points_added": 50000},
                                     format='json')
        response = self.test_view(request, pk=1)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        # Add points with non admin user.
        user = User.objects.get(pk=3)
        request = self.factory.patch('/api/v1/users/1/points/',
                                     data={"points_added": 50000},
                                     format='json')
        force_authenticate(request, user)
        response = self.test_view(request, pk=user.pk)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_spend_points(self):
        # Spend points with admin user.
        admin_user = User.objects.get(pk=1)
        customer_with_points = User.objects.get(pk=2)
        request = self.factory.patch(f'/api/v1/users/{customer_with_points.pk}/points/',
                                     {"points_spent": 5000}, format='json')
        force_authenticate(request, admin_user)
        response = self.test_view(request, pk=customer_with_points.pk)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual({"points": 45000}, response.data)

        # Check updated points with admin user.
        request = self.factory.get(f'/api/v1/users/{customer_with_points.id}/points/')
        force_authenticate(request, admin_user)
        response = self.test_view(request, pk=customer_with_points.pk)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual({"points": 45000}, response.data)

        # Spend points with no authentication.
        request = self.factory.patch(f'/api/v1/users/{customer_with_points.id}/points/',
                                     data={"points_spent": 5000},
                                     format='json')
        response = self.test_view(request, pk=customer_with_points.pk)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        # Spend points with non admin user.
        request = self.factory.patch(f'/api/v1/users/{customer_with_points.id}/points/',
                                     data={"points_spent": 5000},
                                     format='json')
        force_authenticate(request, customer_with_points)
        response = self.test_view(request, pk=customer_with_points.pk)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_not_enough_points(self):
        user = User.objects.get(pk=1)
        request = self.factory.get(f'/api/v1/users/{user.id}/points/')
        force_authenticate(request, user)
        response = self.test_view(request, pk=user.pk)

        original_points = response.data['points']

        request = self.factory.patch(f'/api/v1/users/{user.id}/points/',
                                     data={"points_spent": original_points + 1000},
                                     format='json')
        force_authenticate(request, user)
        response = self.test_view(request, pk=user.pk)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual({"points": "Not enough points."}, response.data)
