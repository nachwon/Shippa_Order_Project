from django.urls import path

from order import views

urlpatterns = [
    path('merchants/<int:merchant_id>/orders/', views.MerchantOrderListCreateView.as_view()),
    path('merchants/<int:merchant_id>/orders/<int:order_id>/', views.MerchantOrderRetrieveUpdateDeleteView.as_view()),
    path('users/<int:user_id>/orders/', views.UserOrderListView.as_view())
]
