from django.contrib import admin
from .models import Offer,Order, OrderItem

admin.site.register(Order)
admin.site.register(Offer)
admin.site.register(OrderItem)

