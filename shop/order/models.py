from django.db import models
from core.models import BaseModel
from product.models import Product
from account.models import User,Address

class Order(BaseModel):
    class OrderStatus(models.TextChoices):
        Delivered = ('d', 'delivered')
        Pending = ('p', 'Pending')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=OrderStatus.choices, default=OrderStatus.Pending)
    timestamp = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    # total_price = 

class ProductOrder(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.PositiveBigIntegerField()
    




