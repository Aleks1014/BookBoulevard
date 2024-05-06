class Cart():
    def __init__(self, request):
        self.session = request.session

        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user is new no session key, so create one.
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make sure cart is available on all pages
        self.cart = cart

    def add(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            pass
        else:
            if product.is_sale:
                price = product.sale_price
            else:
                price = product.price
            self.cart[product_id] = {'price': str(price)}
        self.session.modified = True

    def __len__(self):
        return len(self.cart)