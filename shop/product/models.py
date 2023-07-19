from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.name
    

    
class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    price = models.PositiveBigIntegerField()

    def __str__(self) -> str:
        return self.name
