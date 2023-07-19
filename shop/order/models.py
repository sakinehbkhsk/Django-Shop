from django.db import models
from core.models import BaseModel
from product.models import Product
from account.models import User,Address

class Offer(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.PositiveBigIntegerField()
    code = models.CharField(max_length=100, unique=True)
    discount = models.SmallIntegerField()
    is_available = models.BooleanField()
    min_price = models.PositiveBigIntegerField()
    max_price = models.PositiveBigIntegerField()
    
    # def discount_to_price(self):
    #     if self.discount > 0:
    #         total_price = self.price - (self.price * self.discount / 100)
    #         return float(total_price)
    #     return 0

class Order(BaseModel):
    class OrderStatus(models.TextChoices):
        Delivered = ('d', 'delivered')
        Pending = ('p', 'Pending')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=OrderStatus.choices, default=OrderStatus.Pending)
    timestamp = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    
    def final_price(self):
        total = sum(item.total_price() for item in self.items.all()) 
        if self.offer :
            discount_price = (self.offer/100)*total
            return (total - discount_price)
        return total     


class ProductOrder(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.PositiveBigIntegerField()

    def total_price(self):
        return self.price * self.quantity
    





