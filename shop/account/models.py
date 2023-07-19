from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from core.models import BaseModel
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
    
class Profile(BaseModel):
    GENDER_CHOICE = (('m', 'male'), ('f', 'female'))
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE, null=True, blank=True)
    image = models.ImageField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.first_name} - {self.last_name}'

class Address(BaseModel):
    address = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.address







