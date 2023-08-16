from django.shortcuts import render,redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem, Offer
from .cart import Cart
from .forms import CartAddForm, OfferApplyForm
from product.models import Product
import datetime
from django.contrib import messages
from django.conf import settings
import requests
import json
from django.http import JsonResponse


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


#? sandbox merchant 
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  
CallbackURL = 'http://127.0.0.1:8080/order/verify/'


class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        request.session['order_pay'] = {
            'order_id': order.id,
        }
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.get_total_price(),
            "Description": description,
            "Phone": request.user.phone_number,
            "CallbackURL": CallbackURL,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        try:
            response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

            if response.status_code == 200:
                response_data = response.json()
                if response_data['Status'] == 100:
                    return JsonResponse({'status': True, 'url': ZP_API_STARTPAY + str(response_data['Authority']), 'authority': response_data['Authority']})
                else:
                    return JsonResponse({'status': False, 'code': str(response_data['Status'])})
            return JsonResponse(response_data)
        
        except requests.exceptions.Timeout:
            return JsonResponse({'status': False, 'code': 'timeout'})
        except requests.exceptions.ConnectionError:
            return JsonResponse({'status': False, 'code': 'connection error'})


class OrderVerifyView(LoginRequiredMixin, View):
    def get(self, request, authority):
        order_id = request.session['order_pay']['order_id']
        order = Order.objects.get(id=int(order_id))
        data = {
        "MerchantID": settings.MERCHANT,
        "Amount": order.get_total_price(),
        "Authority": authority,
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return JsonResponse({'status': True, 'RefID': response['RefID']})
            else:
                return JsonResponse({'status': False, 'code': str(response['Status'])})
        return response