from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Custom user manager with email field as unique identifier
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with given password and email    
        """
        if not email:
            raise ValueError('You must provide email')
        normal_email = self.normalize_email(email)
        user = self.model(email = normal_email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        """
        Create and save a Superuser 
        (is_active, is_staff, is_superuser set to True) 
        with given password and email
        """
        superuser_settings = {
            'is_active': True,
            'is_staff': True,
            'is_superuser': True
        }
        user = self.create_user(email, password, **superuser_settings)
        return user