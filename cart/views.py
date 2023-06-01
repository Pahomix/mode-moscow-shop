from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product, Size
from .cart import Cart
from .forms import CartAddProductForm

# Create your views here.

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(product_id, request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        quantity = cd['quantity']
        
        if cd['update']:
            cart.update_quantity(product_id, quantity)
        
        cart.add(
            product=product,
            size=cd['size'],
            quantity=quantity
        )
        
    return redirect('cart:cart_detail')


def cart_remove(request, product_id, size_id):
    cart = Cart(request)
    cart.remove(product_id, size_id)
    cart.save()
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    total_price = 0
    
    for item in cart:
        product_id = item['product_id']
        product = get_object_or_404(Product, id=product_id)
        selected_size = get_object_or_404(Size, id=item['size_id'])
        item['product'] = product
        item['size'] = selected_size

        item_total_price = item['quantity'] * item['product'].price
        total_price += item_total_price

        item['total_price'] = item_total_price
        item['form'] = CartAddProductForm(product_id, initial={'quantity': item['quantity'], 'size': selected_size})

    return render(request, 'cart/cart.html', {'cart': cart, 'total_price': total_price})


