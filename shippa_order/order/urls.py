from django.urls import path
from order.views import OrderListCreateView, OrderRetrieveUpdateDestroyView

from order.admin_views import UpdateOrderStatusView, OrderSalesReportView

urlpatterns = [
    path('<int:order_id>/status/', UpdateOrderStatusView.as_view()),
    path('sales_report/', OrderSalesReportView.as_view()),
    path('self/', OrderListCreateView.as_view()),
    path('<int:id>/', OrderRetrieveUpdateDestroyView.as_view())
]