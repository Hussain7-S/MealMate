"""
A tiny session-based cart.
We keep it simple: session stores {menu_item_id: quantity}.
Nothing fancy, but it does the job without needing a DB hit for every click.
"""
from decimal import Decimal
from restaurants.models import MenuItem

CART_SESSION_KEY = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if not cart:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def add(self, menu_item, quantity=1):
        item_id = str(menu_item.id)
        if item_id in self.cart:
            self.cart[item_id]['quantity'] += quantity
        else:
            self.cart[item_id] = {
                'quantity': quantity,
                'price': str(menu_item.price),
                'restaurant_id': menu_item.restaurant_id,
            }
        self.save()

    def remove(self, menu_item_id):
        item_id = str(menu_item_id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def update(self, menu_item_id, quantity):
        item_id = str(menu_item_id)
        if item_id in self.cart:
            if quantity <= 0:
                self.remove(item_id)
            else:
                self.cart[item_id]['quantity'] = quantity
                self.save()

    def clear(self):
        self.session[CART_SESSION_KEY] = {}
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        item_ids = self.cart.keys()
        menu_items = MenuItem.objects.filter(id__in=item_ids)
        items_map = {str(m.id): m for m in menu_items}
        for item_id, data in self.cart.items():
            menu_item = items_map.get(item_id)
            if not menu_item:
                continue
            price = Decimal(data['price'])
            yield {
                'menu_item': menu_item,
                'quantity': data['quantity'],
                'price': price,
                'subtotal': price * data['quantity'],
            }

    def total(self):
        return sum(Decimal(v['price']) * v['quantity'] for v in self.cart.values())

    def count(self):
        return sum(v['quantity'] for v in self.cart.values())
