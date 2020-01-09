from django.urls import path
from order.views import OrderListCreateView, OrderRetrieveUpdateDestroyView

urlpatterns = [
    path('self/', OrderListCreateView.as_view()),
    path('<int:id>/', OrderRetrieveUpdateDestroyView.as_view())
]