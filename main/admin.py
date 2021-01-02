from django.contrib import admin
from .models import UserDetail, Slider, Contact, Cart
from saler.models import Product, ProductSize, SalerDetail, category, dow, SellerSlider, MyCart, WholeSaleProduct, Orders, trend,WholeSaleProductOrders

admin.site.site_header = 'Wrappers'

admin.site.register(UserDetail)
admin.site.register(Product)
admin.site.register(ProductSize)
admin.site.register(SalerDetail)
admin.site.register(Slider)
admin.site.register(category)
admin.site.register(dow)
admin.site.register(Contact)
admin.site.register(SellerSlider)
admin.site.register(MyCart)
admin.site.register(WholeSaleProduct)
admin.site.register(WholeSaleProductOrders)
admin.site.register(Cart)
admin.site.register(Orders)
admin.site.register(trend)