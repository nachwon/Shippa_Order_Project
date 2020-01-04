from django.urls import path

from merchants.views import MerchantListCreateView, MerchantRetrieveUpdateView, \
    MenuListCreateView, MenuRetrieveUpdateView


urlpatterns = [
    path('', MerchantListCreateView.as_view()),
    path('<int:pk>/', MerchantRetrieveUpdateView.as_view()),
    path('<int:merchant_id>/menus/', MenuListCreateView.as_view()),
    path('<int:merchant_id>/menus/<int:pk>/', MenuRetrieveUpdateView.as_view()),
]
