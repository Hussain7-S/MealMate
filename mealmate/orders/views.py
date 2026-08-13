from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from restaurants.models import MenuItem, Restaurant
from .cart import Cart
from .models import Order, OrderItem


@require_POST
def cart_add(request, item_id):
    cart = Cart(request)
    menu_item = get_object_or_404(MenuItem, id=item_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(menu_item, quantity)
    messages.success(request, f"Added {menu_item.name} to your cart.")
    return redirect(request.POST.get('next', 'restaurants:home'))


@require_POST
def cart_update(request, item_id):
    cart = Cart(request)
    quantity = int(request.POST.get('quantity', 1))
    cart.update(item_id, quantity)
    return redirect('orders:cart_detail')


@require_POST
def cart_remove(request, item_id):
    cart = Cart(request)
    cart.remove(item_id)
    return redirect('orders:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'orders/cart.html', {'cart': cart})


@login_required
def checkout(request):
    cart = Cart(request)
    items = list(cart)
    if not items:
        return redirect('orders:cart_detail')

    restaurant = items[0]['menu_item'].restaurant

    if request.method == 'POST':
        address = request.POST.get('address') or request.user.address
        payment_method = request.POST.get('payment_method', 'cod')
        order = Order.objects.create(
            customer=request.user,
            restaurant=restaurant,
            delivery_address=address,
            payment_method=payment_method,
            is_paid=(payment_method != 'cod'),
        )
        for entry in items:
            OrderItem.objects.create(
                order=order,
                menu_item=entry['menu_item'],
                quantity=entry['quantity'],
                price=entry['price'],
            )
        order.recalc_total()
        cart.clear()
        return redirect('orders:order_confirmation', pk=order.pk)

    return render(request, 'orders/checkout.html', {'cart': cart, 'restaurant': restaurant})


@login_required
def order_confirmation(request, pk):
    order = get_object_or_404(Order, pk=pk, customer=request.user)
    return render(request, 'orders/confirmation.html', {'order': order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})


@login_required
def track_order(request, pk):
    order = get_object_or_404(Order, pk=pk, customer=request.user)
    return render(request, 'orders/track.html', {'order': order})


@login_required
def owner_orders(request):
    if not request.user.is_owner():
        return redirect('restaurants:home')
    orders = Order.objects.filter(restaurant__owner=request.user).order_by('-created_at')
    return render(request, 'orders/owner_orders.html', {'orders': orders})


@login_required
@require_POST
def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk, restaurant__owner=request.user)
    status = request.POST.get('status')
    if status in dict(Order.STATUS_CHOICES):
        order.status = status
        order.save(update_fields=['status'])
    return redirect('orders:owner_orders')
