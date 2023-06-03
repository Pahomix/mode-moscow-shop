from django.http import HttpResponse
from django.shortcuts import render
from .models import OrderItem, ProductSize
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            order_placement_success = False  # Flag to track successful order placement
            for item in cart:
                size_id = item['size_id']
                product_id = item['product'].id
                quantity = item['quantity']
                product_size = ProductSize.objects.filter(product_id=product_id, size_id=size_id).first()
                if not product_size or product_size.quantity < quantity:
                    return HttpResponse('Invalid size or insufficient quantity')
                
                quantity = int(quantity)
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=quantity,
                    size=product_size
                )
                # Set flag to indicate successful order placement
                order_placement_success = True
                # Subtract the quantity selected by the user from the product size
                product_size.quantity -= quantity
                product_size.save()
                # Subtract the quantity selected by the user from the total stock of the product
                product_size.product.stock -= quantity
                product_size.product.save()
            if order_placement_success:
                cart.clear()
                order_created.delay(order.id)
                return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})
