from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from users.views import UserListCreateView, UserRetrieveUpdateDestroyView, PointRetrieveUpdateView

urlpatterns = [
    path('', UserListCreateView.as_view()),
    path('<int:pk>/', UserRetrieveUpdateDestroyView.as_view()),
    path('<int:pk>/points/', PointRetrieveUpdateView.as_view()),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh')
]
