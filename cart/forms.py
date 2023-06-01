from django import forms
from shop.models import Size, Product, ProductSize

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=[], coerce=int, initial=1)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    size = forms.ModelChoiceField(queryset=None, widget=forms.Select(attrs={'id': 'id_size'}))

    def __init__(self, product_id, *args, **kwargs):
        super(CartAddProductForm, self).__init__(*args, **kwargs)
        product = Product.objects.get(id=product_id)
        product_sizes = ProductSize.objects.filter(product=product, quantity__gt=0)
        sizes = Size.objects.filter(id__in=product_sizes.values('size_id'))
        max_quantity = max(product_sizes.values_list('quantity', flat=True))  # Максимальное количество товара
        self.fields['quantity'].choices = [(i, i) for i in range(1, max_quantity + 1)]  # Заполняем список значений для quantity
        self.fields['size'].queryset = sizes

