from django.test import TestCase

from profiles.models import UserProfile, Follow
from django.contrib.auth.models import User

class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='eric12345', email='test1@g.com')
        self.user2 = User.objects.create_user(username='testuser2', password='eric12345', email='test2@g.com')
        self.user_profile1 = UserProfile.objects.create(user=self.user1, bio='test1 bio')
        self.user_profile2 = UserProfile.objects.create(user=self.user2, bio='test2 bio')
    
    def test_user_profile_creation(self):
        self.assertEqual(self.user_profile1.user.username, 'testuser1')
        self.assertEqual(self.user_profile2.user.username, 'testuser2')
        self.assertEqual(self.user_profile1.bio, 'test1 bio')
        self.assertEqual(self.user_profile2.bio, 'test2 bio')

    def test_user_profile_str(self):
        self.assertEqual(str(self.user_profile1), 'testuser1')