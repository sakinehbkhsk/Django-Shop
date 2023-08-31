from django.test import TestCase
from django.urls import reverse
from account.models import User
from django.shortcuts import get_object_or_404
from product.models import Product, Category
from order.cart import Cart
from order.forms import CartAddForm 

# class CartViewTest(TestCase):
#     def test_cart_view(self):
#         user = User.objects.create_user(phone_number='09123456789', password='testpassword', email='a@gmail.com', first_name='ali')
#         self.client.login(phone_number='09123456789', password='testpassword', email='a@gmail.com', first_name='ali')

#         category = Category.objects.create(
#             name='Test Category',
#             slug='test-category',
#             is_sub=False
#         )

#         product = Product.objects.create(
#             name='Test Product',
#             slug='test',
#             image='img1',
#             category='cat',
#             is_available=True,
#             price=10.99,
#             description='aaaa'
#         )
#         product.category.set(category)
#         cart = Cart(self.client.session)
#         cart.add(product)
#         response = self.client.get(reverse('order:cart'))
#         self.assertEqual(response.status_code, 200)


# class CartAddViewTest(TestCase):
#     def test_cart_add_view(self):
#         user = User.objects.create_user(phone_number='09123456789', password='testpassword', email='a@gmail.com', first_name='ali')
#         self.client.login(phone_number='09123456789', password='testpassword', email='a@gmail.com', first_name='ali')

#         category = Category.objects.create(
#             name='Test Category',
#             slug='test-category',
#             is_sub=False
#         )
#         product = Product.objects.create(
#             name='Test Product',
#             slug='test',
#             image='img1',
#             category='cat',
#             is_available=True,
#             price=10.99,
#             description='aaaa'
#         )
#         product.category.set(category)
#         response = self.client.post(reverse('order:cart_add', args=[product.id]), data={'quantity': 2})
#         self.assertRedirects(response, reverse('order:cart'))

# class CartRemoveViewTest(TestCase):
#     def test_cart_remove_view(self):
#         user = User.objects.create_user(phone_number='09123456789', password='testpassword', email='a@gmail.com', first_name='ali')
#         self.client.login(phone_number='09123456789', password='testpassword', email='a@gmail.com', first_name='ali')
#         product = Product.objects.create(
#             name='Test Product',
#             slug='test',
#             image='img1',
#             category='cat',
#             is_available=True,
#             price=10.99,
#             description='aaaa'
#         )
#         cart = Cart(self.client.session)
#         cart.add(product)
#         response = self.client.get(reverse('order:cart_remove', args=[product.id]))
#         self.assertRedirects(response, reverse('order:cart'))
