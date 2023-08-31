from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('', views.ProductView.as_view(), name='product'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:category_slug>/', views.ProductView.as_view(), name='category_filter'),
    path('search_product', views.SearchProduct.as_view(), name='search_product'),

]