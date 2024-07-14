from .wish_list import Wishlist

def wish_list(request):
    return {'wish_list': Wishlist(request)}