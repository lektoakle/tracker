from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import get_sentinel_user

class UserManagerTests(TestCase):

    def test_create_user_(self):
        """New normal user has email as provided
        is active, is not staff, is not superuser"""    
        User = get_user_model()  
        first_name="Amy"
        last_name="Smith"
        user = User.objects.create_user(
            email='test@example.com', 
            password='test123', 
            first_name=first_name, 
            last_name=last_name)
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(str(user), " ".join((user.first_name, user.last_name)))
        self.assertEqual(str(user), "Amy Smith") 
        
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

    def test_create_new_user_normailized(self):
        """New user email is normailized"""
        User = get_user_model()
        email = 'test@EXEMPLE.com'
        user = User.objects.create_user(email=email, password="1234")
        self.assertEqual(user.email, email.lower())

    
class UserTest(TestCase):
    def test_create_sentinel_user(self):
        """If sentinel user does'not exist, 
        create it"""
        sentinel_user = get_sentinel_user()
        self.assertIsNotNone(sentinel_user)
        self.assertEqual(sentinel_user.email, "deleted@user.com")
        


    def test_get_sentinel_user(self):
        """If sentinel user exists,
        get it"""
        sentinel_user = get_user_model().objects.create_user(email="deleted@user.com", password="1234")
        sentinel_user2 = get_sentinel_user()
        self.assertEqual(sentinel_user.id, sentinel_user2.id)