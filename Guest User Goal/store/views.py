from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
import json
import datetime

from rest_framework.generics import GenericAPIView

from .models import *
from .utils import cookieCart, cartData, guestOrder, myOrdersData
from django import forms
from .serializers import (CustomerSerializer)


class StudentForm(forms.Form):
    email = forms.EmailField(label="Enter Email")

class StoreAPiView(GenericAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = CustomerSerializer

def post(self, request, *args, **kwags):
	    data = cartData(request)
	    cartItems = data['cartItems']
	    order = data['order']
	    items = data['items']
	    products = Product.objects.all()
	    context = {'products':products, 'cartItems':cartItems}
	    return render(request, 'store/store.html', context)



class EmailVerifyAPiView(GenericAPIView):
   
    permission_classes = ()
    authentication_classes = ()
    def post(self, request, *args, **kwags):
	    student = StudentForm()
	    return render(request, "store/email_verify.html", {'form': student})


# def index(request):
#
# 	data=submit(request)
# 	print("respinse",data)
# 	return render(request, "store/my_orders.html", {'data': data})


class CartAPiView(GenericAPIView):

    permission_classes = ()
    authentication_classes = ()
    def post(self, request, *args, **kwags):
	    data = cartData(request)
	    cartItems = data['cartItems']
	    order = data['order']
	    items = data['items']
	    context = {'items':items, 'order':order, 'cartItems':cartItems}
	    return render(request, 'store/cart.html', context)

class MyOrdersApiView(GenericAPIView):

	permission_classes = ()
	authentication_classes = ()

	def post(self, request, *args, **kwags):
		if request.user == "AnonymousUser":
			print("AnonymousUser")
		else:
			print("login")
		if request.user.is_authenticated:
			data = myOrdersData(request, request.user.customer.email)
		else:
			if request.method == 'POST':
				data = myOrdersData(request,request.POST['email'])
		cartItems = data['cartItems']
		order = data['order']
		items = data['items']
		context = {'items':items, 'order':order, 'cartItems':cartItems}
		return render(request, 'store/my_orders.html', context)



def verify_email(request):
	data = myOrdersData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}

	return render(request, 'store/email_verify.html', context)


class CheckoutApiView(GenericAPIView):
   
	permission_classes = ()
	authentication_classes = ()

	def post(self, request, *args, **kwags):
		data = cartData(request)

		cartItems = data['cartItems']
		order = data['order']
		items = data['items']

		context = {'items':items, 'order':order, 'cartItems':cartItems}
		return render(request, 'store/checkout.html', context)


class UpdateItemApiView(GenericAPIView):
	
	permission_classes = ()
	authentication_classes = ()

	def post(self, request, *args, **kwags):
		data = json.loads(request.body)
		productId = data['productId']
		action = data['action']
		print('Action:', action)
		print('Product:', productId)

		customer = request.user.customer
		product = Product.objects.get(id=productId)
		order, created = Order.objects.get_or_create(customer=customer, complete=False)

		orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

		if action == 'add':
			orderItem.quantity = (orderItem.quantity + 1)
		elif action == 'remove':
			orderItem.quantity = (orderItem.quantity - 1)

		orderItem.save()

		if orderItem.quantity <= 0:
			orderItem.delete()

		return JsonResponse('Item was added', safe=False)

class ProcessOrderApiView(GenericAPIView):
	
	permission_classes = ()
	authentication_classes = ()

	def post(self, request, *args, **kwags):
		transaction_id = datetime.datetime.now().timestamp()
		data = json.loads(request.body)

		if request.user.is_authenticated:
			customer = request.user.customer
			order, created = Order.objects.get_or_create(customer=customer, complete=False)
		else:
			customer, order = guestOrder(request, data)

		total = float(data['form']['total'])
		order.transaction_id = transaction_id

		if total == order.get_cart_total:
			order.complete = True
		order.save()

		if order.shipping == True:
			ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
			)

		return JsonResponse('Payment submitted..', safe=False)