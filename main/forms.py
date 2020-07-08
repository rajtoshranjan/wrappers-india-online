from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import UserDetail

class UserRegisterForm(UserCreationForm):
	first_name = forms.CharField(widget=forms.TextInput(attrs={}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={}))
	username = forms.CharField(label=("Mobile Number/Email"),widget=forms.TextInput(attrs={'oninput':'validate()'}))
	password1 = forms.CharField(label=("Password"), strip=False, widget=forms.PasswordInput(attrs={}),)
	password2  = forms.CharField(label=("Confirm"), strip=False, widget=forms.PasswordInput(attrs={}),)
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			'first_name',
			 'last_name',
			 'email',
		]

class UpdateUserDetailForm(forms.ModelForm):
	class Meta:
		model = UserDetail
		fields = [
			'dob',
			'photo',
			'mobile',
			'alternate_mobile',
			'address',
			'pincode',
			'landmark',
			'locality',
			'city',
			'state',
			'sex',
		]

class UserAddressForm1(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			'first_name',
			 'last_name',
		]
class UserAddressForm(forms.ModelForm):
	address = forms.CharField(widget=forms.TextInput(attrs={}))
	locality = forms.CharField(required =True)
	city = forms.CharField(required =True)
	alternate_mobile = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Alternate Mobile No(optional)'}), required = False)
	landmark = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Landmark(optional)'}), required = False)
	class Meta:
		model = UserDetail
		fields = [
			'mobile',
			'alternate_mobile',
			'address',
			'pincode',
			'landmark',
			'locality',
			'city',
			'state',
		]
