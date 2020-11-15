from django.test import TestCase
from django.contrib.auth import get_user_model

class UserManagerTests(TestCase):

    def test_create_user_(self):
        """New normal user has email as provided
        is active, is not staff, is not superuser"""    
        User = get_user_model() 
        user = User.objects.create_user(email='test@example.com', password='test123')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        
        self.assertIsNone(user.username)
        
        """if no email is provided, create_user() raises errors"""
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='',password='test123')
        

    def test_create_superuser(self):
        """New superuser has email as provided
        is active, is staff, is superuser"""
        User = get_user_model() 
        user = User.objects.create_superuser(email='test@example.com', password='test123')  
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)