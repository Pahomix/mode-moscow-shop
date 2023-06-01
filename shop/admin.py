from django.contrib import admin
from .models import Category, Product, Size, ProductSize
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)

class SizeAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Size, SizeAdmin)

class ProductSizeFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        
        total_quantity = sum(form.cleaned_data.get('quantity', 0) for form in self.forms)
        
        if total_quantity > self.instance.stock:
            raise ValidationError("The total quantity of sizes cannot exceed the stock quantity of the product.")

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1
    formset = ProductSizeFormSet
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductSizeInline]
admin.site.register(Product, ProductAdmin)