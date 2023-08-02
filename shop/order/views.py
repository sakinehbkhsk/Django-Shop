from django.shortcuts import render,redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem, Offer
from .cart import Cart
from .forms import CartAddForm, OfferApplyForm
from product.models import Product
import datetime
from django.contrib import messages


class CartView(View):
    def get(self,request):
        cart = Cart(request)
        return render(request, 'order/cart.html', {'cart': cart})
     

class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('order:cart')
    

class CartRemoveView(View):
    def get(self,request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('order:cart')
    

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


class OfferApplyView(LoginRequiredMixin,View):
    form_class = OfferApplyForm

    def post(self, request, order_id):
        now = datetime.datetime.now()
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                offer = Offer.objects.get(code__exact=code, start_time__lte=now, end_time__gte=now, active=True)
            except Offer.DoesNotExist:
                messages.error(request, 'this coupon does not exists.', 'danger')
                return redirect('order:order_detail', order_id)
            order = Order.objects.get(id=order_id)
            order.discount = offer.discount
            order.save()
        return redirect('order:order_detail', order_id)
