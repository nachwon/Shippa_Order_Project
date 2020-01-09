from django.urls import path
from order.views import OrderListCreateView, OrderRetrieveUpdateDestroyView

from order.admin_views import UpdateOrderStatusView, OrderSalesReportView, OrderDetailView, OrderListView

urlpatterns = [
    path('order/<int:order_id>/status/', UpdateOrderStatusView.as_view()),
    path('order/sales_report/', OrderSalesReportView.as_view()),
    path('order/self/', OrderListCreateView.as_view()),
    path('<int:id>/', OrderRetrieveUpdateDestroyView.as_view()),
    path('order/detail/', OrderDetailView.as_view()),
    path('order/list/merchant/', OrderListView.as_view())
]