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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from order.tasks import send_order_status_email


class CartView(View):
    def get(self,request):
        cart = Cart(request)
        return render(request, 'order/cart.html', {'cart': cart})
    

# CartAPI
# class CartAPIView(APIView):
#     def get(self, request):
#         cart = Cart(request)
#         cart_data = {
#             'cart_items': list(cart),
#             'cart_total_quantity': len(cart),
#             'cart_total_price': cart.get_total_price(),
#         }
#         return Response(cart_data, status=status.HTTP_200_OK)

     

class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('order:cart')

# CartAddView
# class CartAddAPIView(APIView):
#     def post(self, request, product_id):
#         cart = Cart(request)
#         product = get_object_or_404(Product, id=product_id)
#         form = CartAddForm(request.data) 
#         if form.is_valid():
#             cart.add(product, form.cleaned_data['quantity'])
#             cart_data = {
#                 'cart_items': list(cart),
#                 'cart_total_quantity': len(cart),
#                 'cart_total_price': cart.get_total_price(),
#             }
#             return Response(cart_data, status=status.HTTP_200_OK)
#         else:
#             return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    

class CartRemoveView(View):
    def get(self,request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('order:cart')
    

# CartRemoveAPIView
# class CartRemoveAPIView(APIView):
#     def delete(self, request, product_id):
#         cart = Cart(request)
#         product = get_object_or_404(Product, id=product_id)
#         cart.remove(product)
        
#         cart_data = {
#             'cart_items': list(cart),
#             'cart_total_quantity': len(cart),
#             'cart_total_price': cart.get_total_price(),
#         }

#         return Response(cart_data, status=status.HTTP_200_OK)


    

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

# OrderApi
# class OrderDetailAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     form_class = OfferApplyForm

#     def get(self, request, order_id):
#         order = get_object_or_404(Order, id=order_id)
#         serializer = OrderSerializer(order)
#         return render(request, 'order/order.html', {'order': serializer.data, 'form': self.form_class})





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
CallbackURL = 'http://127.0.0.1:8080/order/order_verify/'


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
                response = response.json()
                if response["Status"] == 100:
                    return redirect(ZP_API_STARTPAY + str(response["Authority"]))
                elif response.get("errors"):
                    e_code = response["errors"]["code"]
                    e_message = response["errors"]["message"]
                    return HttpResponse(
                        f"Error code: {e_code}, Error Message: {e_message}"
                    )
            return HttpResponse(response.items())

        except requests.exceptions.Timeout:
            return {"status": False, "code": "timeout"}
        except requests.exceptions.ConnectionError:
            return {"status": False, "code": "connection error"}
        


class OrderVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        order_id = request.session['order_pay']['order_id']
        order = Order.objects.get(id=int(order_id))
        data = {
        "MerchantID": settings.MERCHANT,
        "Amount": order.get_total_price(),
        "Authority": request.GET["Authority"],
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response["Status"] == 100 or response["Status"] == 101:
                order.status = 2
                order.transaction_id = response["RefID"]
                order.save()
                cart = order.customer.cart
                if cart.coupon:
                    coupon = cart.coupon
                    coupon.is_active = False
                    coupon.save()
                    cart.coupon = None
                    cart.save()

                for item in cart.cart_items.all():
                    product = item.product
                    product.quantity -= item.quantity
                    if product.quantity == 0:
                        product.is_active = False
                    product.save()
                    item.delete()

                if order.user.email:
                    mail = order.user.email
                    message = f"Transaction success.RefID:  {str(response['RefID'])}"
                    mail_subject = "Order Confirmed Successfuly"
                    send_order_status_email.delay(mail, message, mail_subject)

                return HttpResponse(
                    f"Transaction success.RefID:  {str(response['RefID'])}, Status: {response['Status']}, order ID: {order_id}"
                )
            else:
                order.status = 3
                order.save()
                return HttpResponse("Transaction failed, order ID:" + str(order_id))
        return response