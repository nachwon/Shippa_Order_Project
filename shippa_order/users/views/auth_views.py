from django.conf import settings
from django.forms import model_to_dict
from rest_framework import views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from google.oauth2 import id_token
from google.auth.transport import requests

from users.models import User
from users.serializers import CustomTokenObtainPairSerializer

__all__ = [
    "CustomTokenObtainPairView",
    "GoogleLoginView"
]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class GoogleLoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def get_tokens_for_user(user):
        refresh = CustomTokenObtainPairSerializer.get_token(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def post(self, request, *args, **kwargs):
        token = request.data.get('id_token')
        user_info = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)

        email = user_info['email']
        username = email.split("@")[0]
        first_name = user_info['given_name']
        last_name = user_info['family_name']

        user, created = User.objects.get_or_create(
            username=username, email=email, first_name=first_name, last_name=last_name
        )

        jwt = self.get_tokens_for_user(user)

        return Response({
            "user_info": model_to_dict(user),
            **jwt
        })
