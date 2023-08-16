from django.test import TestCase
from django.urls import reverse
from .models import Product, Category
from . import views


class ProductViewTest(TestCase):
    def test_product_list_view(self):
        response = self.client.get(reverse('product:product'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/product.html')
    
    def test_category_filter_view(self):
        category = Category.objects.create(name='Test Product', slug='test')
        response = self.client.get(reverse('product:category_filter', kwargs={'category_slug': category.slug}))
        self.assertEqual(response.status_code, 200)


# class ProductDetailViewTest(TestCase):
#     def setUp(self):
#         self.product = Product.objects.create(name='Test Product', slug='testpro')
    
#     def test_product_detail_view(self):
#         response = self.client.get(reverse('product:product_detail', kwargs={'slug': self.product.slug}))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'product/detail.html')


class SearchProductTest(TestCase):
    def test_search_product_view(self):
        response = self.client.get(reverse('product:search_product'), {'q': 'test query'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/search.html')

    
