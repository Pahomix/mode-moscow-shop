from django.shortcuts import render, get_object_or_404
from .models import Category, Product, ProductSize
from cart.forms import CartAddProductForm
# Create your views here.

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category,
                                     slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/index.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})
    
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm(product_id=id)
    product_sizes = ProductSize.objects.filter(product=product, quantity__gt=0)
    return render(request, 'shop/product/goods.html', {'product': product, 'cart_product_form': cart_product_form, 'product_sizes': product_sizes})