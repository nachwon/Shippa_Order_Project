from django.urls import path

from users.views import UserListCreateView

urlpatterns = [
    path('', UserListCreateView.as_view())
]
