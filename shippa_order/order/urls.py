from django.urls import path
from order.views import OrderListCreateView, OrderRetrieveUpdateDestroyView

from order.admin_views import UpdateOrderStatusView, OrderSalesReportView, OrderDetailView, OrderListView

urlpatterns = [
    path('self/', OrderListCreateView.as_view()),
    path('<int:id>/', OrderRetrieveUpdateDestroyView.as_view()),
    path('admin/detail/', OrderDetailView.as_view()),
    path('admin/order_list/', OrderListView.as_view()),
    path('admin/<int:order_id>/status/', UpdateOrderStatusView.as_view()),
    path('admin/sales_report/', OrderSalesReportView.as_view()),
]