from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, phone_number,password, email=None):
        if not phone_number:
            raise ValueError('Enter a phone number.')
        
        user = self.model(phone_number=phone_number, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, password, email=None):
        user = self.create_user(phone_number, password, email)
        user.is_admin = True
        user.save(using=self._db)
        return user

    


