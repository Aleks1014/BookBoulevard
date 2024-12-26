from django.shortcuts import render, get_object_or_404
from .wish_list import Wishlist
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.

def wish_list_summary(request):
    wish_list = Wishlist(request)
    wish_list_products = wish_list.get_products
    return render(request, 'wish_list_summary.html',
                  {'wish_list_products': wish_list_products, })


def wish_list_add(request):
    wish_list = Wishlist(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        wish_list.add(product=product)
        response = JsonResponse({'Product Name: ': product.title})
        messages.success(request, 'Product was successfully added to your wish list.')
        return response



def wishlist_delete(request):
    wishlist = Wishlist(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        wishlist.delete(product=product_id)
        response = JsonResponse({'product': product_id})
        messages.success(request, 'Product was deleted from your wishlist.')
        return response
