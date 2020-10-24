from django.shortcuts import render
from .models import *


def store(request):
    return render(request, 'store/store.html', {'products': Product.objects.all()})


def cart(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user.customer, completed=False)
        items = order.orderitem_set.all()
    else:
        items, order = [], {'get_total_cart_price': 0, 'get_total_cart_n_items': 0}
    return render(request, 'store/cart.html', {'items': items, 'order': order})


def checkout(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user.customer, completed=False)
        items = order.orderitem_set.all()
    else:
        items, order = [], {'get_total_cart_price': 0, 'get_total_cart_n_items': 0}
    return render(request, 'store/checkout.html', {'items': items, 'order': order})
