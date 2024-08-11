import datetime
from django.shortcuts import render, redirect
from cart.cart import Cart
from order_process.forms import ShippingForm, PaymentForm
from order_process.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from store.models import Product
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid



# Create your views here.


def payment_success(request):
    return render(request, 'payment/payment_success.html', {})

def payment_fail(request):
    return render(request, 'payment/payment_fail.html', {})


def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_products
    quantities = cart.get_quants
    total_price = cart.total()
    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user_id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html',
                      {'cart_products': cart_products, 'quantities': quantities, 'total_price': total_price,
                       'shipping_form': shipping_form})
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html',
                      {'cart_products': cart_products, 'quantities': quantities, 'total_price': total_price,
                       'shipping_form': shipping_form})


def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_products
        quantities = cart.get_quants
        total_price = cart.total()
        # session with shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
        host = request.get_host()
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': total_price,
            'item_name': 'BookBoulevard',
            'invoice': str(uuid.uuid4()),
            'no_shipping': 2,
            'currency_code': 'GBP',
            'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
            'return': 'http://{}{}'.format(host, reverse('payment_success')),
            'cancel': 'http://{}{}'.format(host, reverse('payment_fail')),
        }

        paypal_form = PayPalPaymentsForm(initial=paypal_dict)
        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html',
                          {'cart_products': cart_products, 'quantities': quantities, 'total_price': total_price,
                           'shipping_info': request.POST, 'billing_form': billing_form, 'paypal_form': paypal_form})
        else:
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html',
                          {'cart_products': cart_products, 'quantities': quantities, 'total_price': total_price,
                           'shipping_info': request.POST, 'billing_form': billing_form})


    else:
        messages.error(request, 'Access Denied')
        return redirect('home')


def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_products
        quantities = cart.get_quants
        total_price = cart.total()
        payment_form = PaymentForm(request.POST or None)
        my_shipping = request.session.get('my_shipping')
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        amount_paid = total_price
        full_shipping_address = f'{my_shipping["shipping_address_1"]}\n' \
                                f'{my_shipping["shipping_address_2"]}\n' \
                                f'{my_shipping["shipping_city"]}\n' \
                                f'{my_shipping["shipping_postal_code"]}' \
                                f'\n{my_shipping["shipping_country"]}\n'

        if request.user.is_authenticated:
            user = request.user
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=full_shipping_address,
                                 amount_paid=amount_paid)
            create_order.save()
            order_id = create_order.pk
            for product in cart_products():
                product_id = product.id
                if product.is_sale:
                    product_price = product.sale_price
                else:
                    product_price = product.price
                product_quantity = quantities()[str(product_id)]
                create_order_item = OrderItem(order_id=order_id, product_id=product_id,user=user,
                                              quantity=product_quantity,
                                              price=product_price)
                create_order_item.save()

        else:
            create_order = Order(full_name=full_name, email=email, shipping_address=full_shipping_address,
                                 amount_paid=amount_paid)
            create_order.save()
            order_id = create_order.pk
            for product in cart_products():
                product_id = product.id
                if product.is_sale:
                    product_price = product.sale_price
                else:
                    product_price = product.price
                product_quantity = quantities()[str(product_id)]
                create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=product_quantity,
                                              price=product_price)
                create_order_item.save()
        messages.success(request, 'Order Placed.')
        for key in list(request.session.keys()):
            if key == 'session_key':
                del request.session[key]
        return redirect('home')

    else:
        messages.error(request, 'Access Denied.')
        return redirect('home')



def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        return render(request, 'payment/shipped_dash.html',{'orders': orders})
    else:
        messages.error(request, 'Access Denied.')
        return redirect('home')


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST['shipping_status']
            pk = request.POST['order_id']
            if status:
                now = datetime.datetime.now()
                order = Order.objects.filter(id=pk)
                order.update(shipped=True)
                order.update(date_shipped=now)
                messages.success(request, 'Order shipped.')
                return redirect('not_shipped_dash')
        return render(request, 'payment/not_shipped_dash.html', {'orders': orders})
    else:
        messages.error(request, 'Access Denied.')
        return redirect('home')


def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order=pk)
        if request.POST:
            status = request.POST['shipping_status']
            if status:
                now = datetime.datetime.now()
                order = Order.objects.filter(id=pk)
                order.update(shipped=True)
                order.update(date_shipped=now)
                messages.success(request, 'Order shipped.')
                return redirect('not_shipped_dash')
        return render(request, 'payment/orders.html', {'order': order, 'items': items})
    else:
        messages.error(request, 'Access Denied.')
        return redirect('home')
