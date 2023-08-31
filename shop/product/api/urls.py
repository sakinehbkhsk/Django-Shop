from django.urls import path
from .views import ProductAPIView, SearchProductAPIView


app_name = 'product_api'
urlpatterns = [
    path('api/products/', ProductAPIView.as_view(), name='api-products'),
    path('api/products/<slug:category_slug>/', ProductAPIView.as_view(), name='api-products-by-category'),
    path('search_product/', SearchProductAPIView.as_view(), name='search_product_api'),
]
