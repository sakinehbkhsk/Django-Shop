from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.name
    
class Offer(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.PositiveBigIntegerField()
    code = models.CharField(max_length=100, unique=True)
    discount = models.SmallIntegerField()
    is_available = models.BooleanField()
    
    @property
    def discount_to_price(self):
        if self.discount > 0:
            total_price = self.price - (self.price * self.discount / 100)
            return float(total_price)
        return 0

    
class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
