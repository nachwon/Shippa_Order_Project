from django.urls import path

from merchants.views import MerchantListCreateView, MerchantRetrieveUpdateView, \
    MenuListCreateView, MenuRetrieveUpdateView
from order.admin_views import MerchantOrderListView, MerchantOrderRetrieveDestroy, MerchantOrderSalesReportView, \
    MerchantUpdateOrderStatusView

urlpatterns = [
    path('', MerchantListCreateView.as_view()),
    path('<int:pk>/', MerchantRetrieveUpdateView.as_view()),
    path('<int:merchant_id>/menus/', MenuListCreateView.as_view()),
    path('<int:merchant_id>/menus/<int:pk>/', MenuRetrieveUpdateView.as_view()),
    path('<int:merchant_id>/orders/', MerchantOrderListView.as_view()),
    path('<int:merchant_id>/orders/<int:order_id>/', MerchantOrderRetrieveDestroy.as_view()),
    path('<int:merchant_id>/sales_report/', MerchantOrderSalesReportView.as_view()),
    path('<int:merchant_id>/orders/<int:order_id>/status/', MerchantUpdateOrderStatusView.as_view())
]
