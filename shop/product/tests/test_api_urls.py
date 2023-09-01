from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class ProductAPIViewTest(APITestCase):
    def test_product_api_view(self):
        url = reverse('product_api:api-products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_filter_api_view(self):
        category_slug = 'test-category' 
        url = reverse('product_api:api-products-by-category', kwargs={'category_slug': category_slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

class SearchProductAPIViewTest(APITestCase):
    def test_search_product_api_view(self):
        url = reverse('product_api:search_product_api')
        search_query = 'rose'  
        response = self.client.get(url, {'search_product': search_query})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    def test_search_product_api_view_no_query(self):
        url = reverse('product_api:search_product_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
