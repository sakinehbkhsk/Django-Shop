from django.urls import reverse
from django.test import TestCase
from order.models import Order
from account.models import User


class OrderCreateViewTest(TestCase):
    def test_order_create_view(self):
        user = User.objects.create_user(phone_number='09123456789', password='testpassword', email='a@gmail.com', first_name='ali')
        self.client.login(phone_number='09123456789', password='testpassword', email='a@gmail.com', first_name='ali')

        url = reverse('order:order_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302) 

class OrderDetailViewTest(TestCase):
    def test_order_detail_view(self):
        user = User.objects.create_user(phone_number='09123456789', password='testpassword', email='a@gmail.com', first_name='ali')
        order = Order.objects.create(user=user)

        url = reverse('order:order_detail', args=[order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class OfferApplyViewTest(TestCase):
    def test_offer_apply_view(self):
        user = User.objects.create_user(phone_number='09123456789', password='testpassword', email='a@gmail.com', first_name='ali')
        order = Order.objects.create(user=user)

        url = reverse('order:apply_offer', args=[order.id])
        response = self.client.post(url, data={'code': 'TESTCODE'})
        self.assertEqual(response.status_code, 302)