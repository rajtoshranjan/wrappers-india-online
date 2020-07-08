from django import forms
class CouponForms(forms.Form):
	code = forms.CharField()