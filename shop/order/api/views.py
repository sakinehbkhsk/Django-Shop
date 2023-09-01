from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from order.forms import OfferApplyForm
from order.models import Order, OrderItem, Offer
from order.cart import Cart
from .serializers import OrderSerializer, OfferSerializer
from rest_framework import status
from rest_framework.response import Response
import datetime

# OrderApi
class OrderDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    form_class = OfferApplyForm

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        serializer = OrderSerializer(order)
        return render(request, 'order/order.html', {'order': serializer.data, 'form': self.form_class})


class OrderCreateAPIView(APIView):
    def post(self, request):
        cart = Cart(request)
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            order = serializer.save(user=request.user)
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()

            return Response(
                {'order_id': order.id},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OfferApplyAPIView(APIView):
    serializer_class = OfferSerializer

    def post(self, request, order_id):
        now = datetime.datetime.now()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            try:
                offer = Offer.objects.get(
                    code__exact=code,
                    start_time__lte=now,
                    end_time__gte=now,
                    active=True
                )
            except Offer.DoesNotExist:
                return Response(
                    {'message': 'This coupon does not exist.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            order = get_object_or_404(Order, id=order_id)
            order.discount = offer.discount
            order.save()

            return Response(
                {'message': 'Coupon applied successfully'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






