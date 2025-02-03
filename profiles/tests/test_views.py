from django.test import TestCase
from django.urls import reverse
from profiles.models import UserProfile
from django.contrib.auth.models import User

class TestUserProfileViews(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='eric12345')
        self.user_profile1 = UserProfile.objects.create(user=self.user1, bio='test1 bio')
    
    def test_user_profile_view(self):
        url = reverse('profiles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='testuser1', password='eric12345')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_profile_detail_view(self):
        url = reverse('profile_detail', args=[self.user_profile1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='testuser1', password='eric12345')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)