from django import template
from saler.models import WholeSaleProduct

register = template.Library()

@register.filter(name='split')
def split(str, key):
    return str.split(key)


@register.filter(name='remfl')
def remfl(str1, key):
	if str1 != '' and key != '':
		return str(str1)[int(key):-int(key)]

@register.filter(name='product')
def product(str1, key):
	if str1.split(key)[0] != '':
		ppp = WholeSaleProduct.objects.filter(product_id=str1.split(key)[0]).first()
		return [ppp.product_name,ppp.image1.url,ppp.price]
