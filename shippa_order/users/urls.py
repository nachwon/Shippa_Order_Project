from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from users import views

urlpatterns = [
    path('', views.UserListCreateView.as_view()),
    path('<int:pk>/', views.UserRetrieveUpdateDestroyView.as_view()),
    path('<int:pk>/points/', views.PointRetrieveUpdateView.as_view()),
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('google/login/', views.GoogleLoginView.as_view())
]
