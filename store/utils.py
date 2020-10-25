import json
from .models import *


def cookie_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('Cart:', cart)

    items, total_cart_n_items, total_cart_price, shipping = [], 0, 0, False
    for i in cart:
        try:
            product = Product.objects.get(id=i)
            total_item_price = product.price * cart[i]['quantity']
            items.append({
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'image_url': product.image_url
                },
                'quantity': cart[i]['quantity'],
                'get_total_price': total_item_price
            })
            if not product.digital:
                shipping = True
            total_cart_n_items += cart[i]['quantity']
            total_cart_price += total_item_price
        except:
            pass
    return {
        'items': items,
        'order': {
            'get_total_cart_price': total_cart_price,
            'get_total_cart_n_items': total_cart_n_items,
            'shipping': shipping
        },
        'cart_n_items': total_cart_n_items
    }
