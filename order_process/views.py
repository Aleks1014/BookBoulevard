from django.shortcuts import render

from cart.cart import Cart
from order_process.forms import ShippingForm
from order_process.models import ShippingAddress


# Create your views here.


def payment_success(request):
    return render(request, 'payment/payment_success.html', {})


def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_products
    quantities = cart.get_quants
    total_price = cart.total()
    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user_id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html', {'cart_products': cart_products,
                                                         'quantities': quantities,
                                                         'total_price': total_price,
                                                         'shipping_form': shipping_form})
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html', {'cart_products': cart_products,
                                                         'quantities': quantities,
                                                         'total_price': total_price,
                                                         'shipping_form': shipping_form})
