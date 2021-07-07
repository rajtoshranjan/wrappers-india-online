from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import SalerDetail, Product, ProductSize, SellerSlider, MyCart, WholeSaleProduct, category, Orders, WholeSaleProductOrders
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SalerRegisterForm, SalerAddressForm, UpdateSalerDetailForm, UpdateSalerAccountDetailForm
from main.forms import UserUpdateForm
from django.contrib.auth.decorators import login_required
from math import ceil
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

#This is view of Index Page of Seller in which we Display Whole Sale Products
@login_required
def index(request):
	if request.user.is_superuser or request.user.is_staff:
		allProds = []
		catprods = WholeSaleProduct.objects.values('category', 'product_id')
		cats = {item['category'] for item in catprods}
		for cat in cats:
			prod = WholeSaleProduct.objects.filter(category=cat)
			n = len(prod)
			nSlides = n // 6 + ceil((n / 6) - (n // 6))
			allProds.append([prod, range(1, nSlides), nSlides])
		params = {
				'allProds':allProds,
				'prod':WholeSaleProduct.objects.all()[::-1][:4],
				'sliders':SellerSlider.objects.all(),
				'trending':WholeSaleProduct.objects.all(),
				'cart_element_no' : len([p for p in MyCart.objects.all() if p.user == request.user]),

				}
		return render(request, 'saler/index.html', params)
	else:
		return redirect("/")

# This is View of Dashboard in which we display all orders of the seller and ther status
@login_required
def dashboard(request):
	if request.user.is_superuser or request.user.is_staff:
		if request.method == 'GET':
			odrr = request.GET.get('odrr')
			st = request.GET.get('st')
			if st == 'Cancel':
				o = Orders.objects.filter(order_id=odrr).first()
				o.status = 'Cancel'
				o.save()
			if st == 'Accepted':
				o = Orders.objects.filter(order_id=odrr).first()
				o.status = 'Accepted'
				o.save()
			if st == 'Packed':
				o = Orders.objects.filter(order_id=odrr).first()
				o.status = 'Packed'
				o.save()
			if st == 'Delivered':
				o = Orders.objects.filter(order_id=odrr).first()
				o.status = 'Delivered'
				o.save()
		ordr = [i for i in Orders.objects.filter(saler=request.user) if i.status != 'Cancel' and i.status != 'On The Way' and i.status != 'Delivered'][::-1]
		params = {
				'orders':ordr,
				'dorders': [i for i in Orders.objects.filter(saler=request.user) if i.status != 'Cancel' and i.status == 'On The Way' or i.status == 'Delivered'][::-1],
				'cart_element_no' : len([p for p in MyCart.objects.all() if p.user == request.user]),
				}
		return render(request, 'saler/dashboard.html', params)
	else:
		return redirect("/")

# This is add to cart view of Seller means Whole Sale Products
@login_required
def add_to_cart(request):
	cart_prods = [p for p in MyCart.objects.all() if p.user == request.user]
	card_prods_id =[i.product_id for i in cart_prods]
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		if prod_id in card_prods_id:
			cart_prods[card_prods_id.index(prod_id)].number += WholeSaleProduct.objects.filter(product_id=prod_id)[0].min_Quantity
			cart_prods[card_prods_id.index(prod_id)].save()
			return HttpResponse(len(cart_prods))

		else:
			MyCart(user = request.user, product_id = prod_id, number = WholeSaleProduct.objects.filter(product_id=prod_id)[0].min_Quantity).save()
			return HttpResponse(len(cart_prods)+1)
	else:
		return HttpResponse("")

# This is view for Increasing Quantity of any Product in Cart
@login_required
def plus_element_cart(request):
	cart_prods = [p for p in MyCart.objects.all() if p.user == request.user]
	card_prods_id =[i.product_id for i in cart_prods]
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		if prod_id in card_prods_id:
			cart_prods[card_prods_id.index(prod_id)].number += WholeSaleProduct.objects.filter(product_id=prod_id)[0].min_Quantity
			cart_prods[card_prods_id.index(prod_id)].save()
			subtotal = 0.0
			delev = 0.0
			cart_prods2 = [p for p in MyCart.objects.all() if p.user == request.user]
			for p in cart_prods2:
				subtotal += p.number * WholeSaleProduct.objects.filter(product_id=p.product_id)[0].price
			tax = subtotal*5/100
			datas = {
				'num':MyCart.objects.filter(user=request.user,product_id=prod_id)[0].number,
				'tax':tax,
				'subtotal':subtotal,
				'delev' : delev,
				'total':subtotal+tax+delev,
				}
			return JsonResponse(datas)
	else:
		return HttpResponse("")

# This is view for Decreasing Quantity of any Product in Cart
@login_required
def minus_element_cart(request):
	cart_prods = [p for p in MyCart.objects.all() if p.user == request.user]
	card_prods_id =[i.product_id for i in cart_prods]
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		if prod_id in card_prods_id:
			cart_prods[card_prods_id.index(prod_id)].number -= WholeSaleProduct.objects.filter(product_id=prod_id)[0].min_Quantity
			cart_prods[card_prods_id.index(prod_id)].save()
			subtotal = 0.0
			delev = 0.0
			cart_prods2 = [p for p in MyCart.objects.all() if p.user == request.user]
			for p in cart_prods2:
				subtotal += p.number * WholeSaleProduct.objects.filter(product_id=p.product_id)[0].price
			tax = subtotal*5/100
			datas = {
				'num':MyCart.objects.filter(user=request.user,product_id=prod_id)[0].number,
				'tax':tax,
				'subtotal':subtotal,
				'delev' : delev,
				'total':subtotal+tax+delev,
				}
			return JsonResponse(datas)
	else:
		return HttpResponse("")

# This is view for Deleting a Product from Cart
@login_required
def delete_from_cart(request):
	cart_prods = [p for p in MyCart.objects.all() if p.user == request.user]
	card_prods_id =[i.product_id for i in cart_prods]
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		if prod_id in card_prods_id:
			cart_prods[card_prods_id.index(prod_id)].delete()
			subtotal = 0.0
			delev = 0.0
			cart_prods2 = [p for p in MyCart.objects.all() if p.user == request.user]
			for p in cart_prods2:
				subtotal += p.number * WholeSaleProduct.objects.filter(product_id=p.product_id)[0].price
			tax = subtotal*5/100
			datas = {
				'len':len(cart_prods2),
				'tax':tax,
				'subtotal':subtotal,
				'delev' : delev,
				'total':subtotal+tax+delev,
				}
			return JsonResponse(datas)
	else:
		return HttpResponse("")

# This view for Display a Single Product 
@login_required
def productView(request, prod_id):
	if request.user.is_superuser or request.user.is_staff:
		params = {
			'product':WholeSaleProduct.objects.filter(product_id = prod_id)[0],
			'cart_element_no' : len([p for p in MyCart.objects.all() if p.user == request.user]),
		}
		return render(request, 'saler/productview.html', params)
	else:
		return redirect("/")

# This is View of Display all Products of a perticular category
@login_required
def view_all(request, catg):
	if request.user.is_superuser or request.user.is_staff:
		params = {
			'product':[i for i in WholeSaleProduct.objects.all() if str(i.category) == catg],
			'catg':catg,
			'cart_element_no' : len([p for p in MyCart.objects.all() if p.user == request.user]),
			}
		return render(request, 'saler/view_all.html', params)
	else:
		return redirect("/")

# seller cart view
@login_required
def mycart(request):
	if request.user.is_superuser or request.user.is_staff:
		allProds = []
		subtotal = 0.0
		delev = 0.0
		cart_prods = [p for p in MyCart.objects.all() if p.user == request.user]
		for p in cart_prods:
			subtotal += p.number * WholeSaleProduct.objects.filter(product_id=p.product_id)[0].price
		tax = subtotal*5/100

		for cprod in cart_prods:
			prod = WholeSaleProduct.objects.filter(product_id=cprod.product_id)[0]
			allProds.append([cprod, prod])
		params = {
					'allProds':allProds,
					'cart_element_no' : len([p for p in MyCart.objects.all() if p.user == request.user]),
					'total':subtotal+tax+delev,
					'subtotal':subtotal,
					'tax':tax,
					'delev':delev,
				}
		return render(request,'saler/cart.html', params)
	else:
		return redirect("/")

# seller checkout view means for whole sale products
def checkout(request):
	if request.user.is_superuser or request.user.is_staff:
		allProds = []
		cart_prods = [p for p in MyCart.objects.all() if p.user == request.user]
		for cprod in cart_prods:
			prod = WholeSaleProduct.objects.filter(product_id=cprod.product_id)[0]
			allProds.append([cprod, prod])
		if request.method == 'POST':
			address_form = SalerAddressForm(request.POST, instance=request.user.salerdetail)
			if address_form.is_valid():
				address_form.save()
				for item in cart_prods:
					if WholeSaleProductOrders.objects.all().last():
						order_id = 'WSPOrder'+str((WholeSaleProductOrders.objects.all().last().pk)+1)
					else:
						order_id = 'WSPOrder001'
					product1 = item.product_id+'|'+str(item.number)+','
					WholeSaleProductOrders(order_id=order_id,user=request.user,products=product1).save()
					item.delete()
				return redirect('seller_orders')
		else:
			address_form = SalerAddressForm(instance=request.user.salerdetail)

		subtotal = 0.0
		delev = 0.0
		for p in cart_prods:
			subtotal += p.number * WholeSaleProduct.objects.filter(product_id=p.product_id)[0].price
		tax = subtotal*5/100
		params = {
				'allProds':allProds,
				'cart_element_no' : len(cart_prods),
				'address_form': address_form,
				'total':subtotal+tax+delev,
			}
		return render(request, 'saler/checkout.html', params)
	else:
		return redirect("/")

# Orders of Seller (Whole sale product)
def MyOrders(request):
	if request.method == 'POST':
		order_id = request.POST.get('order_id')
		o = WholeSaleProductOrders.objects.filter(order_id=order_id)[0]
		o.status = 'Cancel'
		o.save()
	params = {
		'orders': [i for i in WholeSaleProductOrders.objects.all() if i.user == request.user and i.status != 'Delivered' and i.status != 'Cancel'],
		'delivered': [i for i in WholeSaleProductOrders.objects.all() if i.user == request.user and i.status == 'Delivered'],
		'cancel': [i for i in WholeSaleProductOrders.objects.all() if i.user == request.user and i.status == 'Cancel'],

	}
	return render(request,'saler/myorders.html', params)

# for adding a new product by seller 
@login_required
def add_product(request):
	if request.user.is_superuser or request.user.is_staff:
		if request.method == 'POST':
			prod_name = request.POST.get('prod_name')
			desc = request.POST.get('desc')
			cat = request.POST.get('category')
			subcategory = request.POST.get('subcategory')
			price = request.POST.get('price')
			price_not = request.POST.get('price_not')
			gst_l = request.POST.get('gst')
			if Product.objects.all():
				prod_id2 = 'pr'+hex(Product.objects.all().last().product_id+1)
			else:
				prod_id2 = 'pr'+hex(0)
			image1 = request.FILES.get("image1")
			image2 = request.FILES.get("image2")
			image3 = request.FILES.get("image3")
			image4 = request.FILES.get("image4")
			image5 = request.FILES.get("image5")
			size_no = int(request.POST.get('size_no'))
			i=1
			sizes=[]
			while i <= size_no:
				if request.POST.get(f'size{i}'):
					sizes.append([request.POST.get(f'size{i}'),int(request.POST.get(f'quantity{i}'))])
				i+=1
			Product(product_id2=prod_id2,shop=request.user,product_name=prod_name,category=category.objects.get(id=int(cat)),subcategory=subcategory,price=price,price_not=price_not,desc=desc,gst=gst_l,image1=image1).save()
			p = Product.objects.filter(product_id2=prod_id2)[0]
			if image2:
				p.image2=image2
			if image3:
				p.image3=image3
			if image4:
				p.image4=image4
			if image5:
				p.image5=image5
			p.save()
			for siz in sizes:
				ProductSize(product=p,size=siz[0],quantity=siz[1]).save()
			messages.success(request, f'Product Added !')
		prod = [p for p in Product.objects.all() if p.shop == request.user]

		if request.method == 'GET':
			pro_id = request.GET.get('pro_id', 0)
			del_prod = [p.product_id for p in Product.objects.all() if p.shop == request.user]
			if int(pro_id) in del_prod:
				Product.objects.filter(product_id=int(pro_id))[0].delete()
				messages.success(request, f'The Product of id {pro_id} is deleted !')
				return redirect('/seller/add_product/')

		subcat=[]
		for cat in category.objects.all():
			x = cat.sub_Categories.split(',')
			x.insert(0, cat)
			subcat.append(x)
		params = {
			'prod':prod[::-1][0:20],
			'cart_element_no' : len([p for p in MyCart.objects.all() if p.user == request.user]),
			'subcat':subcat,
			}
		return render(request, 'saler/add_product.html',params)
	else:
		return redirect("/")

# it will display all products of a seller
@login_required
def view_products(request):
	if request.user.is_superuser or request.user.is_staff:
		prod = [p for p in Product.objects.all() if p.shop == request.user]

		if request.method == 'GET':
			pro_id = request.GET.get('pro_id')
			if pro_id:
				del_prod = [p.product_id for p in Product.objects.all() if p.shop == request.user]
				if int(pro_id) in del_prod:
					Product.objects.filter(product_id=int(pro_id))[0].delete()
					messages.success(request, f'The Product of id {pro_id} is deleted !')
					return redirect('/seller/view_products/')

		params = {
			'prod': prod[::-1],
			'cart_element_no' : len([p for p in MyCart.objects.all() if p.user == request.user]),
			}
		return render(request, 'saler/view_products.html',params)
	else:
		return redirect("/")

# Signup for Seller
def seller_signup(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			form = SalerRegisterForm(request.POST)
			if form.is_valid():
				form.save();
				username = form.cleaned_data.get('username')
				shop = form.cleaned_data.get('shop')
				gst = form.cleaned_data.get('gst')
				usr = User.objects.filter(username=username).first()
				usr.is_staff=True
				usr.save()
				if username.isdigit():
					SalerDetail(user=usr,mobile=username,gst_Number=gst,shop_Name=gst).save()
				else:
					usr.email = username
					usr.save()
					SalerDetail(user=usr,gst_Number=gst,shop_Name=gst).save()
				messages.success(request, f'Account is Created for {username}')
				return redirect('login')
		else:
			form = SalerRegisterForm()
	return render(request, 'saler/seller_signup.html', {'form':form, 'title':'Become a Seller'})

# Seller Account Settings
@login_required
def account_settings(request):
	if request.user.is_superuser or request.user.is_staff:
		if request.method == 'POST':
			#User Details Update
			s_form = UpdateSalerDetailForm(request.POST, request.FILES, instance=request.user.salerdetail)
			u_form = UserUpdateForm(request.POST, instance=request.user)
			if s_form.is_valid() and u_form.is_valid():
				s_form.save()
				u_form.save()
				messages.success(request, f'Your Account has been Updated!')
				return redirect("saler_account_settings")

			#Change Password
			pass_change_form = PasswordChangeForm(request.user, request.POST)
			if pass_change_form.is_valid():
				user = pass_change_form.save()
				update_session_auth_hash(request, user)  # Important!
				messages.success(request, 'Your password was successfully updated!')
				return redirect('saler_account_settings')
			else:
				messages.error(request, 'Please correct the error below.')

			#Account Settings
			acc_form = UpdateSalerAccountDetailForm(request.POST, request.FILES, instance=request.user.salerdetail)
			if acc_form.is_valid():
				acc_form.save()
				messages.success(request, f'Account Settings has been Updated!')
				return redirect("saler_account_settings")

		else:
			s_form = UpdateSalerDetailForm(instance=request.user.salerdetail)
			u_form = UserUpdateForm(instance=request.user)
			acc_form = UpdateSalerAccountDetailForm(instance=request.user.salerdetail)
			pass_change_form = PasswordChangeForm(request.user)
		detl = {
			'u_form':u_form,
			's_form':s_form,
			'pass_change_form':pass_change_form,
			'acc_form':acc_form,
			'cart_element_no' : len([p for p in MyCart.objects.all() if p.user == request.user]),
			'title':'User Account Settings',
			}
		return render(request, 'saler/account_settings.html', detl)
	else:
		return redirect("/")

# This is a part of admin view in which all ordered products will display with address
def admin2(request):
	if request.user.is_superuser:
		ordr = [i for i in Orders.objects.all() if i.status != 'Cancel' and i.status != 'On The Way' and i.status != 'Delivered'][::-1]
		params = {
				'orders':ordr,
				'dorders': [i for i in Orders.objects.filter(saler=request.user) if i.status != 'Cancel' and i.status == 'On The Way' or i.status == 'Delivered'],
				'cart_element_no' : len([p for p in MyCart.objects.all() if p.user == request.user]),
				}
		return render(request, 'saler/admin2.html', params)
	else:
		return redirect("/")
