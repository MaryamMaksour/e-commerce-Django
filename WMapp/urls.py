from django.urls import path
from .views import *

app_name = "WMapp"

urlpatterns = [
    path('', HomeView.as_view(), name = "home"),
    path('Wemen/', WemenView.as_view(), name = "Wemen"),
    path('Sport/', SportView.as_view(), name = "Sport"),
    path('Outwears/', OutwearsView.as_view(), name = "Outwears"),
    path('checkout/', CheckoutView.as_view(), name = "checkout"),
    path('order-summary/', OrderSummaryView.as_view(), name = "order-summary"),
    path('product/<slug>/', ItemDetailView.as_view(), name = "product"),
    path('add_to_cart/<slug>/', add_to_cart, name = "add_to_cart"),
    path('remove_from_cart/<slug>/', remove_from_cart, name = "remove_from_cart"),
    path('remove_single_item_from_cart/<slug>/', remove_single_item_from_cart, 
            name = "remove_single_item_from_cart"),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund')

]
