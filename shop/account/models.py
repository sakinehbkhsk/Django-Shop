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

class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=20, unique=True)
    email =  models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'phone_number'
    
    def __str__(self):
        return self.phone_number
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self,app_lable):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    

    




