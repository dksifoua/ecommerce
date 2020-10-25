let updateButtons = document.getElementsByClassName('update-cart');

for (let i = 0; i < updateButtons.length; i++) {
    updateButtons[i].addEventListener('click', function () {
        let productId = this.dataset.product
        let action = this.dataset.action
        console.log('ProductId:', productId, 'Action:', action)

        if (user === 'AnonymousUser') {
            console.log('AnonymousUser')
        } else {
            updateUserOrder(productId, action)
        }
    })
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
