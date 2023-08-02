from django.db import models
from core.models import BaseModel
from product.models import Product
from account.models import User
from django.core.validators import MinValueValidator, MaxValueValidator



class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    discount = models.IntegerField(blank=True, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('paid', '-updated')

    def __str__(self):
        return f'{self.user} - {str(self.id)}'

    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount_price = (self.discount / 100) * total
            return int(total - discount_price)
        return total    


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.PositiveBigIntegerField()

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity


class Offer(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.PositiveBigIntegerField()
    code = models.CharField(max_length=100, unique=True)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(90)])
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.code
    





