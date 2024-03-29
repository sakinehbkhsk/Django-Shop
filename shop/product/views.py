from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Product, Category
from order.forms import CartAddForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .api.serializers import CategorySerializer, ProductSerializer
from rest_framework import generics
from django.views.generic import TemplateView
from rest_framework.generics import ListAPIView
from django.db.models import Sum


#View class
# class ProductView(View):
#     def get(self, request, category_slug=None):
#         products = Product.objects.filter(is_available=True)
#         categories = Category.objects.filter(is_sub=False)
#         if category_slug:
#             category = Category.objects.get(slug=category_slug)
#             products = products.filter(category=category)
#         return render(request, 'product/product.html', {'products':products, 'categories':categories})

from django.views.generic import ListView
from django.core.paginator import Paginator

class ProductView(ListView):
    template_name = 'product/product.html'
    context_object_name = 'products'
    paginate_by = 2  

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        products = Product.objects.filter(is_available=True)
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_sub=False)
        return context

    

class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = CartAddForm()
        return render(request, 'product/detail.html', {'product': product, 'form': form})



class SearchProduct(ListView):
    model = Product
    template_name = 'product/search.html'
    context_object_name = 'products'

    def get_queryset(self):
        search_products = self.request.GET.get('search_product')
        top_selling = top_selling_products = Product.objects.annotate(total_quantity=Sum('name')).order_by('-total_quantity')[:10]
        if search_products:
            products = Product.objects.filter(name__icontains = search_products)
            return products


