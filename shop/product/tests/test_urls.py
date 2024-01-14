from django.test import TestCase
from django.urls import reverse
from product.models import Category 

class ProductUrlsTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
            slug='your-category-slug'
        )

    def test_product_view_url(self):
        url = reverse('product:product')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_category_filter_view_url(self):
        category_slug = 'your-category-slug'
        url = reverse('product:category_filter', kwargs={'category_slug': category_slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_search_product_view_url(self):
        url = reverse('product:search_product')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
