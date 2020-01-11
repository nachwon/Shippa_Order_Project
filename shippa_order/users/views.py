import requests

from django.forms import model_to_dict
from rest_framework import generics, permissions, views, status, exceptions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import UserSerializer, PointSerializer, CustomTokenObtainPairSerializer
from users import permissions as custom_permissions


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [custom_permissions.IsAdminOrSelf]


class PointRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = PointSerializer
    queryset = User.objects.all()
    permission_classes = [custom_permissions.IsSelfReadOnlyOrAdmin]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class GoogleLoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def google_oauth(self, access_token):
        user_info_request_uri = 'https://www.googleapis.com/oauth2/v2/userinfo'
        headers = {'Bearer': access_token}
        params = {
            'access_token': access_token
        }
        response = requests.get(user_info_request_uri, headers=headers, params=params)

        if response.status_code != status.HTTP_200_OK:
            raise exceptions.AuthenticationFailed("Invalid 'access_token'.")

        return response.json()

    @staticmethod
    def get_tokens_for_user(user):
        refresh = CustomTokenObtainPairSerializer.get_token(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def post(self, request, *args, **kwargs):
        access_token = request.data.get('access_token')
        user_info = self.google_oauth(access_token=access_token)
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
