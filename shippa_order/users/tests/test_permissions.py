from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from users.views import PointRetrieveUpdateView


User = get_user_model()


class TestPermissions(TestCase):
    factory = None
    test_view = None

    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.test_view = PointRetrieveUpdateView.as_view()

        User.objects.create(id=1, username="admin_user", is_superuser=True, is_staff=True)
        User.objects.create(id=2, username="user_with_points", points=50000)
        User.objects.create(id=3, username="user_with_no_points")
