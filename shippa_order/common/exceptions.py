from rest_framework.exceptions import APIException
from rest_framework import status


from common.error_codes import ErrorCodes


# Users
class UsersException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_code = ErrorCodes.USER.value


# Merchants
class MerchantsException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_code = ErrorCodes.MERCHANT.value


class MerchantIsUnavailable(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'You cannot use this merchant.'
    default_code = ErrorCodes.MERCHANT.value + 101


class MenuIsUnavailable(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'You cannot purchase this menu.'
    default_code = ErrorCodes.MERCHANT.value + 102


# Orders
class OrdersException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'Order Service is Unavailable'
    default_code = ErrorCodes.ORDER.value


class OrderCanCelFailedException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Order cancellation failed'
    default_code = ErrorCodes.ORDER.value


# Notifications
class NotificationsException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = ErrorCodes.NOTIFICATION.value
