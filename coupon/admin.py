from django.contrib import admin
from .models import CouponCode
# Register your models here.
class CouponAdmin(admin.ModelAdmin):
	list_display = ['code','valid_from','valid_to','discounts','active']
	list_filter = ['active','valid_from','valid_to']
	search_fields = ['code']

admin.site.register(CouponCode,CouponAdmin)