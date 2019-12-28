from django.urls import path, re_path

from users.views import UserListCreateView, UserRetrieveUpdateDestroyView, PointRetrieveUpdateView

urlpatterns = [
    path('', UserListCreateView.as_view()),
    re_path(r'^(?P<pk>[a-f0-9]{32})/$', UserRetrieveUpdateDestroyView.as_view()),
    re_path(r'^(?P<pk>[a-f0-9]{32})/points/$', PointRetrieveUpdateView.as_view())
]
