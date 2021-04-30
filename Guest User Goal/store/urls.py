from django.urls import path
from django.conf.urls import url
from .views import (StoreAPiView, MyOrdersApiView, CheckoutApiView, ProcessOrderApiView, UpdateItemApiView,
					EmailVerifyAPiView, CartAPiView)

from . import views

urlpatterns = [
	#Leave as empty string for base url
	url('', StoreAPiView.as_view(), name='store'),

	path('cart/', CartAPiView.as_view(), name="cart"),

	url('my_orders/', MyOrdersApiView.as_view(), name='my_orders'),

	url('email_verify/', EmailVerifyAPiView.as_view(), name='email_verify'),

	url('checkout/', CheckoutApiView.as_view(), name='checkout'),

	url('update_item/', UpdateItemApiView.as_view(), name='update_item'),

	url('process_order/', ProcessOrderApiView.as_view(), name='process_order'),

]