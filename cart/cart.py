from decimal import Decimal
from django.conf import settings
from shop.models import Product, ProductSize

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart or not isinstance(cart, dict):  # Изменено условие проверки на список
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        
    def add(self, product, size, quantity=1, update_quantity=False):
        product_id = str(product.id)
        size_id = str(size.id)
        cart_item = self.cart.get(f"{product_id}_{size_id}")
        
        if cart_item:
            if update_quantity:
                cart_item['quantity'] = quantity
            else:
                cart_item['quantity'] += quantity
        else:
            self.cart[f"{product_id}_{size_id}"] = {
                'product_id': product_id,
                'size_id': size_id,
                'quantity': quantity,
                'price': str(product.price),
                'size': size.name,
            }
        
        self.save()



        
    def save(self):
        self.session.modified = True

    def remove(self, product_id, size_id):
        product_id = str(product_id)
        size_id = str(size_id)
        cart_items = list(self.cart.values())
        for item in cart_items:
            if item['product_id'] == product_id and item['size_id'] == size_id:
                del self.cart[f"{product_id}_{size_id}"]
                break
        self.save()
            
    def __iter__(self):
        product_ids = [item['product_id'] for item in self.cart.values()]
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for cart_item in cart.values():
            product_id = cart_item['product_id']
            product = products.get(id=product_id)
            cart_item['product'] = product
            cart_item['price'] = Decimal(cart_item['price'])
            cart_item['total_price'] = cart_item['price'] * cart_item['quantity']
            cart_item['product_id'] = int(cart_item['product_id'])
            yield cart_item

    def update_quantity(self, product_id, quantity):
        product_id = str(product_id)
        cart_item = self.cart.get(product_id)
        
        if cart_item:
            cart_item['quantity'] = quantity
            self.save()
                
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        return sum(Decimal(item['total_price']) for item in self.cart.values())

        
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
        
        