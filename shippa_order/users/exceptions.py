from rest_framework import status
from rest_framework.exceptions import APIException


class BadRequest(APIException):
    default_detail = "Bad request."
    status_code = status.HTTP_400_BAD_REQUEST
