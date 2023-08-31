from rest_framework.response import Response
from rest_framework.views import APIView
from product.models import Product
from .serializers import ProductSerializer
from rest_framework import status



# APIView
class ProductAPIView(APIView):
    def get(self, request, category_slug=None):
        products = Product.objects.filter(is_available=True)
        if category_slug:
            products = products.filter(category__slug=category_slug)
        ser_data = ProductSerializer(instance=products, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class SearchProductAPIView(APIView):
    def get(self, request, format=None):
        search_query = self.request.GET.get('search_product')
        if search_query:
            products = Product.objects.filter(name__icontains = search_query)
            ser_data = ProductSerializer(products, many=True)
            return Response(ser_data.data, status=status.HTTP_200_OK)

        return Response({'error': 'search query not found.'}, status=status.HTTP_400_BAD_REQUEST)