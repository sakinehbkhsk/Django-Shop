from django.urls import path
from .views import OrderDetailAPIView, OrderCreateAPIView, OfferApplyAPIView


app_name = 'order_api'
urlpatterns = [
    path('api/detail/<int:order_id>/', OrderDetailAPIView.as_view(), name='order_detail_api'),
    path('api/orders/create/', OrderCreateAPIView.as_view(), name='order-create-api'),
    path('api/orders/<int:order_id>/apply-offer/', OfferApplyAPIView.as_view(), name='offer-apply-api'),
]

