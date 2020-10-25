from django.shortcuts import render
from django.http import JsonResponse

import json
import datetime
from .models import *
from .utils import cookie_cart


def store(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user.customer, completed=False)
        context = {
            'products': Product.objects.all(),
            'cart_n_items': order.get_total_cart_n_items
        }
    else:
        cookie_data = cookie_cart(request)
        context = {
            'products': Product.objects.all(),
            'cart_n_items': cookie_data['cart_n_items']
        }
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user.customer, completed=False)
        items = order.orderitem_set.all()
        context = {
            'items': items,
            'order': order,
            'cart_n_items': order.get_total_cart_n_items
        }
    else:
        context = cookie_cart(request)
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user.customer, completed=False)
        items = order.orderitem_set.all()
        context = {
            'items': items,
            'order': order,
            'cart_n_items': order.get_total_cart_n_items
        }
    else:
        cookie_data = cookie_cart(request)
        context = {
            'items': cookie_data['items'],
            'order': cookie_data['order'],
            'cart_n_items': cookie_data['cart_n_items']
        }
    return render(request, 'store/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']
    print(f'product id: {product_id} - action: {action}')

    customer = request.user.customer
    product = Product.objects.get(id=product_id)

    order, created = Order.objects.get_or_create(customer=customer, completed=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity += 1
    elif action == 'remove':
        order_item.quantity -= 1
    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()
    return JsonResponse(f'{action} item done!', safe=False)


def process_order(request):
    data = json.loads(request.body)
    transaction_id = datetime.datetime.now().timestamp()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
    else:
        print('User is not logged in!')
        print('Cookies:', request.COOKIES)

        name = data['form']['name']
        email = data['form']['email']

        customer, created = Customer.objects.get_or_create(email=email)
        customer.name = name
        customer.save()

        order = Order.objects.create(customer=customer, completed=False)
        cookie_data = cookie_cart(request)
        items = cookie_data['items']
        for item in items:
            product = Product.objects.get(id=item['product']['id'])
            _ = OrderItem.objects.create(order=order, product=product, quantity=item['quantity'])

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == order.get_total_cart_price:
        order.completed = True
    order.save()

    if order.shipping:
        ShippingAddress.objects.create(customer=customer,
                                       order=order,
                                       address=data['shipping']['address'],
                                       city=data['shipping']['city'],
                                       state=data['shipping']['state'],
                                       zipcode=data['shipping']['zipcode'])
    return JsonResponse('Process order ...', safe=False)
