from django.test import TestCase
from django.urls import reverse
from order.models import Offer
from django.core.exceptions import ValidationError
from django.utils import timezone



class CartViewTest(TestCase):
    def test_cart_view(self):
        response = self.client.get(reverse('order:cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order/cart.html')


class OfferModelTest(TestCase):
    def setUp(self):
        self.offer_data = {
            'start_time': timezone.now(),
            'end_time': timezone.now() + timezone.timedelta(days=7),
            'price': 1000,
            'code': 'SUMMER2023',
            'discount': 20,
            'active': True,
        }

    def test_create_offer(self):
        offer = Offer(**self.offer_data)
        offer.save()
        self.assertEqual(Offer.objects.count(), 1)
        self.assertEqual(str(offer), 'SUMMER2023')

    def test_unique_code(self):
        offer1 = Offer(**self.offer_data)
        offer1.save()

        offer2 = Offer(**self.offer_data)
        with self.assertRaises(ValidationError):
            offer2.full_clean()

    def test_discount_validation(self):
        self.offer_data['discount'] = -10
        with self.assertRaises(ValidationError):
            offer = Offer(**self.offer_data)
            offer.full_clean()

        self.offer_data['discount'] = 100
        with self.assertRaises(ValidationError):
            offer = Offer(**self.offer_data)
            offer.full_clean()

    def test_inactive_offer(self):
        self.offer_data['active'] = False
        offer = Offer(**self.offer_data)
        offer.save()
        self.assertFalse(offer.active)
