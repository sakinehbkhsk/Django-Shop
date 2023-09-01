from django.test import TestCase
from account.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()



class ProfileModelTest(TestCase):
    def test_profile_str(self):
        user = User.objects.create_user(phone_number='1234567890', email='test@example.com', first_name='John', password='testpassword')
        profile = Profile.objects.create(user=user, first_name='John', last_name='Doe')
        self.assertEqual(str(profile), 'John - Doe')
