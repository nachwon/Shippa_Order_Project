from django.urls import path

from order.views import UpdateOrderStatusView, OrderSalesReportView

urlpatterns = [
    path('<int:order_id>/status/', UpdateOrderStatusView.as_view()),
    path('sales_report/', OrderSalesReportView.as_view())
]