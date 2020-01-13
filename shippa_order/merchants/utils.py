from decimal import Decimal

from common.datetimes import get_utc_datetime, get_day_from_datetime, get_time_from_datetime
from common.exceptions import MerchantIsUnavailable, MenuIsUnavailable
from merchants.models import Merchant, Menu


def _check_if_menu_is_belong_to_merchant(merchant_id, merchant_id_of_menu):
    if merchant_id != merchant_id_of_menu:
        raise MenuIsUnavailable


def _check_if_merchant_is_forced_closing(merchant_forced_closing):
    if merchant_forced_closing:
        raise MerchantIsUnavailable


def _check_business_days(merchant_business_days, datetime_now):
    if not (merchant_business_days & get_day_from_datetime(datetime_now)):
        raise MerchantIsUnavailable


def _is_now_between_start_t_with_end_t(start_t, end_t, now_t):
    return True if start_t < now_t < end_t else False


def _check_open_and_close_time(merchant_open_time, merchant_close_time, datetime_now):

    if merchant_open_time == merchant_close_time:
        return

    time_now = get_time_from_datetime(datetime_now)

    # day open
    if merchant_open_time < merchant_close_time:
        if _is_now_between_start_t_with_end_t(
                start_t=merchant_open_time,
                end_t=merchant_close_time,
                now_t=time_now
        ):
            return
        raise MerchantIsUnavailable

    # night open
    if not _is_now_between_start_t_with_end_t(
            start_t=merchant_close_time,
            end_t=merchant_open_time,
            now_t=time_now
    ):
        return
    raise MerchantIsUnavailable


def _check_if_menu_is_closed(menu_closed):
    if menu_closed:
        raise MenuIsUnavailable


class MenuManager:

    def __init__(self, merchant_id, menu_ids, discount_policy_name="MMT_EMPLOYEE"):
        self.merchant_id = merchant_id
        self.menu_ids = menu_ids
        self.discount_ratio = discount_policy_name

        self._set_data()

    def _set_data(self):
        self.merchant = Merchant.objects.get(pk=self.merchant_id)
        self.menus = [Menu.objects.get(pk=menu_id) for menu_id in self.menu_ids]
        if len(self.menus) != len(self.menu_ids):
            raise Menu.DoesNotExist

    @property
    def merchant_id(self):
        return self._merchant_id

    @merchant_id.setter
    def merchant_id(self, value):
        self._merchant_id = value

    @property
    def menu_ids(self):
        return self._menu_ids

    @menu_ids.setter
    def menu_ids(self, value):
        self._menu_ids = value

    @property
    def discount_ratio(self):
        return self._discount_ratio

    @discount_ratio.setter
    def discount_ratio(self, value):
        self._discount_ratio = 0.5 if value == "MMT_EMPLOYEE" else 1

    def check_if_menus_order_is_available(self):
        datetime_now = get_utc_datetime()

        # check if menu is belong to merchant
        any(_check_if_menu_is_belong_to_merchant(self.merchant_id, menu.merchant.id) for menu in self.menus)

        # check if merchant is forced closing
        _check_if_merchant_is_forced_closing(self.merchant.forced_closing)

        # check if business days
        _check_business_days(self.merchant.business_days, datetime_now)

        # check open and close time
        _check_open_and_close_time(self.merchant.open_time, self.merchant.close_time, datetime_now)

        # check if menus is closed
        any(_check_if_menu_is_closed(menu.closed) for menu in self.menus)

    def get_menus_for_order(self):
        """
            {
                43: {
                    menu_id: 43,
                    merchant_id: 15,
                    name: "Americano - HOT",
                    price: 3000,
                    currency: "KRW",
                    quantity: 0,
                    discounted_price: 1500,
                    discount_ratio: 0.5,
                },
                44: {...}, ...
            }

            quantity '0' is unlimited

        :return: menus for order
        :rtype: _MenuForOrder
        """

        return {
            menu.id: _MenuForOrder(
                menu_id=menu.id, merchant_id=menu.merchant.id, name=menu.name,
                price=menu.price, currency=menu.currency, quantity=menu.quantity,
                discounted_price=round(Decimal(str(menu.price)) * (Decimal('1') - Decimal(str(self.discount_ratio)))),
                discount_ratio=self.discount_ratio
            ) for menu in self.menus
        }


class _MenuForOrder:
    def __init__(
            self, menu_id, merchant_id, name, price, currency, quantity, discounted_price, discount_ratio
    ):
        self.menu_id = menu_id
        self.merchant_id = merchant_id
        self.name = name
        self.price = price
        self.currency = currency
        self.quantity = quantity
        self.discounted_price = discounted_price
        self.discount_ratio = discount_ratio

    @property
    def menu_id(self):
        return self._menu_id

    @menu_id.setter
    def menu_id(self, value):
        self._menu_id = value

    @property
    def merchant_id(self):
        return self._merchant_id

    @merchant_id.setter
    def merchant_id(self, value):
        self._merchant_id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, value):
        self._currency = value

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        self._quantity = value

    @property
    def discounted_price(self):
        return self._discounted_price

    @discounted_price.setter
    def discounted_price(self, value):
        self._discounted_price = value

    @property
    def discount_ratio(self):
        return self._discount_ratio

    @discount_ratio.setter
    def discount_ratio(self, value):
        self._discount_ratio = value
