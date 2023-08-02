from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from core.models import BaseModel
from .managers import UserManager

class User(AbstractBaseUser,PermissionsMixin):
    email = models.CharField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    first_name = models.CharField(max_length=225)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'first_name']

    def __str__(self):
        return self.email
    
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


class OtpCode(BaseModel):
    phone_number = models.CharField(max_length=11)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    




