let updateButtons = document.getElementsByClassName('update-cart');

for (let i = 0; i < updateButtons.length; i++) {
    updateButtons[i].addEventListener('click', function () {
        let productId = this.dataset.product
        let action = this.dataset.action
        console.log('ProductId:', productId, 'Action:', action)

        if (user === 'AnonymousUser') {
            addCookieItem(productId, action)
        } else {
            updateUserOrder(productId, action)
        }
    })
}

function addCookieItem(productId, action) {
    console.log('AnonymousUser')
    if (cart === null)
        cart = {}
    if (action === 'add') {
        if (cart[productId] === undefined)
            cart[productId] = {'quantity': 1}
        else
            cart[productId]['quantity'] += 1
    }
    if (action === 'remove') {
        cart[productId]['quantity'] -= 1
        if (cart[productId]['quantity'] <= 0) {
            console.log('Item should be delete!')
            delete cart[productId]
        }
    }
    console.log('cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
    location.reload()
}

function updateUserOrder(productId, action) {
    console.log('User authenticated. Sending data ...')
    fetch('/update-item/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            'productId': productId,
            'action': action
        })
    }).then(response => response.json()).then(data => {
        console.log('Data:', data)
        location.reload()
    })
}
