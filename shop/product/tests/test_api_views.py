from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from product.models import Product,Category

class ProductAPIViewTest(APITestCase):
    def setUp(self):
        # Create a test product
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            description='This is a test product.',
            price=10.99,
            is_available=True,
        )

    def test_product_api_view(self):
        url = reverse('product_api:api-products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  

    def test_category_filter_api_view(self):

        category_slug = 'test-category'
        category = Category.objects.create(
            name='Test Category',
            slug=category_slug,
        )
        self.product.category.set([category])

        url = reverse('product_api:api-products-by-category' , kwargs={'category_slug': category_slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class SearchProductAPIViewTest(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            description='This is a test product.',
            price=10.99,
            is_available=True,
        )

    def test_search_product_api_view(self):
        url = reverse('product_api:search_product_api')
        search_query = 'Test Product'
        response = self.client.get(url, {'search_product': search_query})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  

    def test_search_product_api_view_no_query(self):
        url = reverse('product_api:search_product_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'search query not found.'})
