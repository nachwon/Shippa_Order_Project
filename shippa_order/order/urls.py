from django.urls import path
from order.views import OrderListCreateView, OrderRetrieveUpdateDestroyView

from order.admin_views import MerchantOrderSalesReportView, MerchantOrderRetrieveDestroy, MerchantOrderListView

urlpatterns = [
    path('self/', OrderListCreateView.as_view()),
    path('<int:id>/', OrderRetrieveUpdateDestroyView.as_view()),
    path('merchant/<int:merchant_id>/orders/<int:order_id>/', MerchantOrderRetrieveDestroy.as_view()),
    path('merchant/<int:merchant_id>/orders/', MerchantOrderListView.as_view()),
    path('merchant/<int:merchant_id>/sales_report/', MerchantOrderSalesReportView.as_view()),
]