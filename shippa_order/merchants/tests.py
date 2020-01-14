import pprint
import mock

from django.test import TestCase
from merchants.models import Merchant, Menu
from merchants.utils import MenuManager


pp = pprint.PrettyPrinter(indent=4)


def _mock_get_utc_datetime():
    from datetime import datetime
    return datetime.strptime('2020-01-20 11:15:27.243860', '%Y-%m-%d %H:%M:%S.%f')


class MerchantTestCase(TestCase):
    def setUp(self):
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
            name='아메리카노 - ICE', price=3000, currency='KRW', quantity=0,
            merchant=self.merchant, closed=False
        )

    @mock.patch('merchants.utils.get_utc_datetime', side_effect=_mock_get_utc_datetime)
    def test_check_if_menus_order_is_available(self, get_utc_datetime_function):
        menu_manager = MenuManager(merchant_id=self.merchant.id, menu_ids=[self.menu1.id, self.menu2.id])
        menu_manager.check_if_menus_order_is_available()
        menus_for_order = menu_manager.get_menus_for_order()
