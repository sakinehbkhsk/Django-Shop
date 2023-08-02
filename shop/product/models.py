from django.db import models
from core.models import BaseModel

class Category(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.name
    
# selfrelation to category
    
class Product(BaseModel):
    name = models.CharField(max_length=200)
    image = models.ImageField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    price = models.PositiveBigIntegerField()

    def __str__(self) -> str:
        return self.name
