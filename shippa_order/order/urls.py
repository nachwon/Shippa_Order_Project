from django.urls import path
from order.views import OrderListCreateView, OrderRetrieveUpdateDestroyView

from order.admin_views import OrderSalesReportView, OrderRetrieveDestroy, OrderListView

urlpatterns = [
    path('self/', OrderListCreateView.as_view()),
    path('<int:id>/', OrderRetrieveUpdateDestroyView.as_view())
]