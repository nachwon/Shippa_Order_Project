import requests

from django.conf import settings
from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import generics, permissions, views
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import UserSerializer, PointSerializer, CustomTokenObtainPairSerializer


class UserListCreateView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]


class PointRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = PointSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class GoogleLoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def google_oauth(self, code):
        redirect_uri = "http://127.0.0.1:8000/api/v1/users/google/login/"

        params_access_token = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
        }
        url_access_token = 'https://www.googleapis.com/oauth2/v4/token'

        response = requests.post(url_access_token, params=params_access_token)
        token_data = response.json()

        access_token = token_data.get('access_token')
        user_info_request_uri = 'https://www.googleapis.com/oauth2/v2/userinfo'
        headers = {'Bearer': access_token}
        params = {
            'access_token': access_token
        }
        user_info = requests.get(user_info_request_uri, headers=headers, params=params)
        return user_info.json()

    @staticmethod
    def get_tokens_for_user(user):
        refresh = CustomTokenObtainPairSerializer.get_token(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        user_info = self.google_oauth(code=code)
        email = user_info['email']
        username = email.split("@")[0]
        first_name = user_info['given_name']
        last_name = user_info['family_name']

        user, created = User.objects.get_or_create(
            username=username, email=email, first_name=first_name, last_name=last_name
        )
        if created:
            user.set_password('test123')
            user.save()

        jwt = self.get_tokens_for_user(user)

        return render(request, 'logged_in.html', {
            "user_info": model_to_dict(user),
            **jwt
        })


class GoogleLoginHTMLView(views.APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'google_login.html')
