from store.models import Product


class Wishlist():
    def __init__(self, request):
        self.session = request.session
        self.request = request

        # Get current session key
        wish_list = self.session.get('wish_list')

        if 'wish_list' not in request.session:
            wish_list = self.session['wish_list'] = {}

        self.wish_list = wish_list


    def add(self, product):
        product_id = str(product.id)
        if product_id in self.wish_list:
            pass
        else:
            if product.is_sale:
                price = product.sale_price
            else:
                price = product.price
            self.wish_list[product_id] = {'price': str(price)}
        self.session.modified = True



    def get_products(self):
        product_ids = self.wish_list.keys()
        products = Product.objects.filter(id__in=product_ids)

        return products