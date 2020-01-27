from enum import Enum

from rest_framework import status
from rest_framework.exceptions import APIException

from rest_framework.views import exception_handler


# def custom_exception_handler(exc, context):
#     # Call REST framework's default exception handler first,
#     # to get the standard error response.
#     response = exception_handler(exc, context)
#     print('context: ', context)
#     print('exc: ', exc.get_full_details())
#     print('response: ', response)
#
#     # Now add the HTTP status code to the response.
#     if response is not None:
#         print('response_data: ', response.data)
#         response.data['description'] = response.data['detail']
#         response.data['status_code'] = response.status_code
#
#     return response


class ObjectDoesNotExists(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Object Does not Exists'


class InvalidParameter(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid parameter.'
