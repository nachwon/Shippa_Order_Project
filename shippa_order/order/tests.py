from django.test import TestCase
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, force_authenticate

from merchants.models import Merchant, Menu
from order.models import Order, OrderItem
from order.views import OrderListCreateView, OrderRetrieveUpdateDestroyView
from users.models import User, PointsLog


class TestOrder(TestCase):
    _base_points = 50000

    def setUp(self) -> None:
        self.api_factory = APIRequestFactory()

        self.merchant = Merchant.objects.create(
            name='MAMU', email='abc@gmail.com', phone='01012341234', forced_closing=False,
            business_days=127, open_time='00:30:00', close_time='14:00:00',
            country_iso='KR', city='서울', detail_address='강남구 논현동 KP Tower'
        )
        self.menu1 = Menu.objects.create(
            name='아메리카노 - HOT', price=3000, currency='KRW', quantity=0,
            merchant=self.merchant, closed=False
        )
        self.menu2 = Menu.objects.create(
            name='아메리카노 - ICE', price=3500, currency='KRW', quantity=0,
            merchant=self.merchant, closed=False
        )

        self.user = User.objects.create(id=1,
                                        username="admin_user",
                                        points=self._base_points)

    def create_order(self, payload: dict = None) -> Response:
        payload = payload if payload else {
            "user": self.user.id,
            "merchant": self.merchant.id,
            "order_items": [{"menu_id": self.menu1.id, "quantity": 5},
                            {"menu_id": self.menu2.id, "quantity": 3}]
        }
        view = OrderListCreateView.as_view()
        request = self.api_factory.post('/api/v1/orders/self/', data=payload, format='json')
        force_authenticate(request, user=self.user)

        return view(request)

    def order_list(self) -> Response:
        view = OrderListCreateView.as_view()
        request = self.api_factory.get('/api/v1/orders/self/')
        force_authenticate(request, user=self.user)

        return view(request)

    def cancel_order(self, order_id: int) -> Response:
        view = OrderRetrieveUpdateDestroyView.as_view()
        request = self.api_factory.delete(path=f'/api/v1/orders/{order_id}/')
        force_authenticate(request, user=self.user)

        return view(request, id=order_id)

    def get_user(self) -> User:
        return User.objects.get(id=self.user.id)

    def test_user_request_order(self):
        create_response = self.create_order()

        order_item_objects = OrderItem.objects.select_related('order').filter(order=create_response.data['order_id'])
        order_object = Order.objects.select_related('user').get(id=create_response.data['order_id'])

        assert create_response.status_code == status.HTTP_201_CREATED

        for order_item in order_item_objects:
            assert order_item.total_price == order_item.discounted_price * order_item.quantity

        # Check User Points
        assert order_object.user.points == self._base_points - order_object.total_price

        # Check Points Log
        points_log_objects = PointsLog.objects.filter(user=self.user)
        assert len(points_log_objects) == 1
        assert points_log_objects[0].points_spent == order_object.total_price

        # Order List Test
        order_list_response = self.order_list()

        assert order_list_response.status_code == status.HTTP_200_OK

    def test_success_cancel_order(self):
        order_id = self.create_order().data['order_id']
        before_user_points = self.get_user().points

        self.cancel_order(order_id=order_id)

        after_user_points = self.get_user().points
        order_object = Order.objects.get(id=order_id)

        # Check Order
        assert order_object.status == 'CANCELED'

        # Check User Points
        assert before_user_points != after_user_points
        assert before_user_points + Order.objects.get(id=order_id).total_price == after_user_points
        assert after_user_points == self._base_points

        # Check Points Log
        points_log = PointsLog.objects.filter(user=self.user.id)
        assert points_log[0].points_spent == order_object.total_price
        assert points_log[1].points_added == order_object.total_price

    def test_failed_cancel_order(self):
        order_id = self.create_order().data['order_id']
        Order.objects.filter(id=order_id).update(status='INPROGRESS')

        cancel_response = self.cancel_order(order_id=order_id)

        assert cancel_response.status_code == status.HTTP_400_BAD_REQUEST

    def test_order_detail_permission(self):
        user2 = User.objects.create(id=2,
                                    username="other_user",
                                    points=self._base_points)

        order_id = self.create_order().data['order_id']

        view = OrderRetrieveUpdateDestroyView.as_view()
        request = self.api_factory.get(path=f'/api/v1/orders/{order_id}/')
        force_authenticate(request, user=self.user)

        # Check Owner Permission
        owner_response = view(request, id=order_id)
        assert owner_response.status_code == status.HTTP_200_OK

        # Check Wrong user Permission
        force_authenticate(request, user=user2)
        other_user_response = view(request, id=order_id)
        assert other_user_response.status_code == status.HTTP_403_FORBIDDEN








