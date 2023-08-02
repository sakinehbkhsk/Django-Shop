from django.shortcuts import render,redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem
from .cart import Cart
from .forms import CartAddForm, OfferApplyForm


class OrderDetailView(LoginRequiredMixin, View):
    form_class = OfferApplyForm

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'order/order.html', {'order':order, 'form':self.form_class})


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
        cart.clear()
        return redirect('order:order_detail', order.id)
