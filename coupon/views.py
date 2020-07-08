from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CouponCode
from .forms import CouponForms
# Create your views here.

@login_required
def coupon_apply(request):
	now = timezone.now()
	form = CouponForms()
	if form.is_valid():
		code = form.cleaned_data['code']
		try:
			coupon = CouponCode.objects.get(code_iexact=code,valid_from_lte=now,valid_to_gte=now,active=True)
			request.session['coupon_id'] = coupon_id
		except CouponCode.DoesNotExist:
			request.session['coupon_id'] = None
	return redirect('cart:cart_details')