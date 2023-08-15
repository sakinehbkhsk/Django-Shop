from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Product, Category
from order.forms import CartAddForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CategorySerializer, ProductSerializer
from rest_framework import generics
from django.views.generic import TemplateView
from rest_framework.generics import ListAPIView


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
    paginate_by = 2  # Adjust the number of products per page as needed

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

    

# APIView
# class ProductAPIView(APIView):
#     def get(self, request, category_slug=None):
#         products = Product.objects.filter(is_available=True)
#         if category_slug:
#             products = products.objects.filter(category__slug=category_slug)
#         ser_data = ProductSerializer(instance=products, many=True)
#         return Response(ser_data.data, status=status.HTTP_200_OK)
    

#GenericAPIView
# class ProductListView(ListAPIView):
#     serializer_class = ProductSerializer

#     def get_queryset(self):
#         queryset = Product.objects.filter(is_available=True)
#         category_slug = self.kwargs.get('category_slug')
#         if category_slug:
#             category = Category.objects.get(slug=category_slug)
#             queryset = queryset.filter(category=category)
#         return queryset

# class ProductView(TemplateView):
#     template_name = 'product/product.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['categories'] = Category.objects.filter(is_sub=False)
#         return context
    

class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = CartAddForm()
        return render(request, 'product/detail.html', {'product': product, 'form': form})



class SearchProduct(ListView):
    model = Product
    template_name = 'search.html'
    context_object_name = 'products'

    def get_queryset(self):
        search_products = self.request.GET.get('search_product')
        top_selling = top_selling_products = Product.objects.annotate(total_quantity=Sum('product_order__number')).order_by('-total_quantity')[:10]
        if search_products:
            products = Product.objects.filter(name__icontains = search_products)
            return products

