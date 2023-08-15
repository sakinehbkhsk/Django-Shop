from django.urls import path
# from .views import ProductListView, ProductView
from . import views


app_name = 'product'
urlpatterns = [
    path('', views.ProductView.as_view(), name='product'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:category_slug>/', views.ProductView.as_view(), name='category_filter'),
    path('search_product', views.SearchProduct.as_view(), name='search_product'),

    # path('api/products/', ProductAPIView.as_view(), name='api-products'),
    # path('api/products/<slug:category_slug>/', ProductAPIView.as_view(), name='api-products-by-category'),

    # path('', ProductListView.as_view(), name='api-products'),
    # path('api/products/<slug:category_slug>/', ProductListView.as_view(), name='api-products-by-category'),
    
]