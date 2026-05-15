from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Customer, Product, Cart, Payment, OrderPlaced, Wishlist
from django.urls import reverse
from django.utils.html import format_html

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'discounted_price',
        'category',
        'product_image'
    ]


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'locality',
        'city',
        'state',
        'pincode'
    ]


from django.urls import reverse
from django.utils.html import format_html


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'products',
        'quantity'
    ]
    def products(self, obj):
        link = reverse("admin:app_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.title)

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'amount',
        'payment_status',
        'paid'
    ]


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'user',
        'customers',
        'products',
        'quantity',
        'ordered_date',
        'status',
    ]

    def customers(self,obj):
        link = reverse("admin:app_customer_change",args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>',link,obj.customer.name)
    
    def products(self, obj):
        link = reverse("admin:app_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.title)

@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'products']   
    def products(self, obj):
        link = reverse("admin:app_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.title)
    
admin.site.unregister(Group)  