from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UpdateUserDetailForm, UserUpdateForm, UserAddressForm, UserAddressForm1
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserDetail, Slider, Contact, Cart
from django.contrib.auth.decorators import login_required
from saler.models import Product, ProductSize, dow, category, Orders, trend, ProductReview
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.csrf import csrf_exempt
from .PayTm import Checksum

def index(request):
	if request.user.is_superuser:
		return redirect('admin2')
	elif request.user.is_staff:
		return redirect("saler_home")
	else:
		pass

	prod = Product.objects.all()
	allProds = []
	catprods = Product.objects.values('category', 'product_id')
	cats = {item['category'] for item in catprods}
	for cat in cats:
		prod = []
		for p in [i for i in Product.objects.filter(category=cat)]:
			prod.append([p,[item for item in ProductSize.objects.filter(product=p)]])
		n = len(prod)
		nSlides = 5
		allProds.append([prod[::-1], range(1, nSlides), nSlides])
	params = {
		'sliders':Slider.objects.all(),
		'allProds':allProds,
		'category':category.objects.all(),
		#'prod_men' : [i for i in prod if i.buyer_gender == 'Male'],
		#'prod_women' : [i for i in prod if i.buyer_gender == 'Female'],
		#'prod_other' : [i for i in prod if i.buyer_gender == 'All'],
		'dow' : dow.objects.all()[0:30],
		'trend': trend.objects.order_by('-number')[0:30],
		'cart_element_no' : len([p for p in Cart.objects.all() if p.user == request.user]),
	}
	return render(request, 'main/index.html', params)

def register(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			form = UserRegisterForm(request.POST)
			if form.is_valid():
				form.save();
				username = form.cleaned_data.get('username')
				usr = User.objects.filter(username=username).first()
				if username.isdigit():
					UserDetail(user=usr,mobile=username).save()
				else:
					usr.email = username
					usr.save()
					UserDetail(user=usr).save()
				messages.success(request, f'Account is Created for {username}')
				return redirect('login')
		else:
			form = UserRegisterForm()
	return render(request, 'main/signup.html', {'form':form, 'title':'Sign Up','category':category.objects.all()})

@login_required
def account_settings(request):
	if request.method == 'POST':
		#User Details Update
		s_form = UpdateUserDetailForm(request.POST, request.FILES, instance=request.user.userdetail)
		u_form = UserUpdateForm(request.POST, instance=request.user)
		if s_form.is_valid() and u_form.is_valid():
			s_form.save()
			u_form.save()
			messages.success(request, f'Your Account has been Updated!')
			return redirect("account_settings")

		#Change Password
		pass_change_form = PasswordChangeForm(request.user, request.POST)
		if pass_change_form.is_valid():
			user = pass_change_form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, 'Your password was successfully updated!')
			return redirect('account_settings')
		else:
			messages.error(request, 'Please correct the error below.')

	else:
		s_form = UpdateUserDetailForm(instance=request.user.userdetail)
		u_form = UserUpdateForm(instance=request.user)
		pass_change_form = PasswordChangeForm(request.user)
	detl = {
		'u_form':u_form,
		's_form':s_form,
		'pass_change_form':pass_change_form,
		'title':'User Account Settings',
		'cart_element_no' : len([p for p in Cart.objects.all() if p.user == request.user]),
		'category':category.objects.all(),
		}
	return render(request, 'main/account_settings.html', detl)

def productView(request, prod_id):
	if request.method == 'POST' and request.user.is_authenticated:
		prod = Product.objects.filter(product_id = prod_id).first()
		review = request.POST.get('review')
		ProductReview(user=request.user,product=prod,review=review).save()
		return redirect(f"/product/{prod_id}")

	prod = Product.objects.filter(product_id = prod_id).first()
	params = {
		'product':prod,
		'product_review': ProductReview.objects.filter(product = prod),
		'sizes':[item for item in ProductSize.objects.filter(product=Product.objects.filter(product_id = prod_id)[0])],
		'cart_element_no' : len([p for p in Cart.objects.all() if p.user == request.user]),
		'category':category.objects.all(),
	}
	return render(request, 'main/single.html', params)


def view_all(request, catg):
	if catg=='dow':
		params = {
			'product':[i for i in dow.objects.all()][::-1],
			'catg':'Deal of the Week',
			'cart_element_no' : len([p for p in Cart.objects.all() if p.user == request.user]),
			'category':category.objects.all(),
			}
		return render(request, 'main/view_dow.html', params)
	elif catg=='trend':
		prod = []
		for p in trend.objects.order_by('number'):
			prod.append([p.product,[item for item in ProductSize.objects.filter(product=p.product)]])
		params = {
			'product':prod,
			'catg':'Treanding',
			'cart_element_no' : len([p for p in Cart.objects.all() if p.user == request.user]),
			'category':category.objects.all(),
			}
		return render(request, 'main/view_all.html', params)
	else:
		prod = []
		for p in [i for i in Product.objects.all() if str(i.category) == catg]:
			prod.append([p,[item for item in ProductSize.objects.filter(product=p)]])
		params = {
			'product':prod,
			'catg':catg,
			'cart_element_no' : len([p for p in Cart.objects.all() if p.user == request.user]),
			'category':category.objects.all(),
			}
	return render(request, 'main/view_all.html', params)


def search(request):
	query = request.GET.get('query', '')
	prods = []
	for prod in [i for i in Product.objects.all() ]:
		if query.lower() in prod.product_name.lower() or query.lower() in prod.desc.lower() or query.lower() in prod.subcategory.lower():
			prods.append([prod,[item for item in ProductSize.objects.filter(product=prod)]])
	params = {
		'product':prods,
		'cart_element_no' : len([p for p in Cart.objects.all() if p.user == request.user]),
		'category':category.objects.all(),
		}
	return render(request, 'main/view_all.html', params)

cart_item_local = []

def dummy_cart(request):
	if request.method == 'GET':
		prod_list = request.GET['prod_list']
		prod_list = prod_list.split(',')
		if request.user.is_authenticated:
			cart_prods = [p for p in Cart.objects.all() if p.user == request.user]
			card_prods_id =[i.product_id for i in cart_prods]
			if len(prod_list) >= 1 and prod_list != ['']:
				for item in prod_list:
					pppp = item.split('|')
					if pppp[0] in card_prods_id:
						cart_prods[card_prods_id.index(pppp[0])].number = int(pppp[1])
						cart_prods[card_prods_id.index(pppp[0])].save()
					else:
						Cart(user = request.user, product_id = pppp[0], number = int(pppp[1])).save()
		else:
			global cart_item_local
			cart_item_local = prod_list
	return HttpResponse("data sebd from py")

@login_required
def cart(request):
	if request.user.is_authenticated:
		allProds = []
		subtotal = 0.0
		delev = 0.0
		tax = 0.0
		cart_prods = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_prods:
			tempTotal = p.number * Product.objects.filter(product_id=p.product_id)[0].price
			subtotal += tempTotal
			tax += tempTotal*int(Product.objects.filter(product_id=p.product_id).first().gst)/100

		for cprod in cart_prods:
			prod = Product.objects.filter(product_id=cprod.product_id)[0]
			allProds.append([cprod, prod])
		params = {
					'allProds':allProds,
					'cart_element_no' : len([p for p in Cart.objects.all() if p.user == request.user]),
					'total':subtotal+tax+delev,
					'subtotal':subtotal,
					'tax':tax,
					'delev':delev,
					'category':category.objects.all(),
				}
		return render(request,'main/cart.html', params)

@login_required
def add_to_cart(request):
	cart_prods = [p for p in Cart.objects.all() if p.user == request.user]
	card_prods_id =[i.product_id for i in cart_prods]
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		prod_id = prod_id.split(',')
		for item in cart_prods:
			if prod_id[0] == item.product_id and prod_id[1] == item.product_size:
				item.number += 1
				item.save()
				return HttpResponse(len(cart_prods))
		Cart(user = request.user, product_id = int(prod_id[0]),product_size=prod_id[1], number = 1).save()
		return HttpResponse(len(cart_prods)+1)
	else:
		return HttpResponse("")

@login_required
def plus_element_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(id=prod_id)
		c.number+=1
		c.save()
		subtotal = 0.0
		delev = 0.0
		tax = 0.0
		cart_prods2 = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_prods2:
			tempTotal = p.number * Product.objects.filter(product_id=p.product_id)[0].price
			subtotal += tempTotal
			tax += tempTotal*int(Product.objects.filter(product_id=p.product_id).first().gst)/100

		datas = {
			'num':Cart.objects.get(id=prod_id).number,
			'tax':tax,
			'subtotal':subtotal,
			'delev' : delev,
			'total':subtotal+tax+delev,
			}
		return JsonResponse(datas)
	else:
		return HttpResponse("")

@login_required
def minus_element_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(id=prod_id)
		c.number-=1
		c.save()
		subtotal = 0.0
		delev = 0.0
		tax = 0.0
		cart_prods2 = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_prods2:
			tempTotal = p.number * Product.objects.filter(product_id=p.product_id)[0].price
			subtotal += tempTotal
			tax += tempTotal*int(Product.objects.filter(product_id=p.product_id).first().gst)/100

		datas = {
			'num':Cart.objects.get(id=prod_id).number,
			'tax':tax,
			'subtotal':subtotal,
			'delev' : delev,
			'total':subtotal+tax+delev,
			}
		return JsonResponse(datas)
	else:
		return HttpResponse("")


@login_required
def delete_from_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(id=prod_id)
		c.delete()
		subtotal = 0.0
		delev = 0.0
		tax = 0.0
		cart_prods2 = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_prods2:
			tempTotal = p.number * Product.objects.filter(product_id=p.product_id)[0].price
			subtotal += tempTotal
			tax += tempTotal*int(Product.objects.filter(product_id=p.product_id).first().gst)/100

		datas = {
			'num':len(cart_prods2),
			'tax':tax,
			'subtotal':subtotal,
			'delev' : delev,
			'total':subtotal+tax+delev,
			}
		return JsonResponse(datas)
	else:
		return HttpResponse("")

MERCHANT_KEY = 'YOUR_MERCHANT_KEY'
@login_required
def order_now(request):
	allProds =[]
	if request.method == 'GET':
		new_prod = request.GET.get('prod_id')
		prod_size = request.GET.get('prod_size')
		allProds = [[1,Product.objects.filter(product_id=int(new_prod))[0]]]
	if request.method == 'POST':
		new_prod = request.GET.get('prod_id')
		prod_size = request.GET.get('prod_size')
		address_form = UserAddressForm(request.POST, instance=request.user.userdetail)
		u_form2 = UserAddressForm1(request.POST, instance=request.user)
		if address_form.is_valid() and u_form2.is_valid():
			address_form.save()
			u_form2.save()
			pay_mode = request.POST.get('pay_mode')
			trends = [i.product.product_id for i in trend.objects.all()]
# 			print(order)
			if pay_mode == 'on':
				if Orders.objects.all().last():
					order_id = 'ordr'+str((Orders.objects.all().last().pk)+1)
				else:
					order_id = 'ordr001'
				product1 = new_prod+'|'+str(1)+','
				Orders(order_id=order_id,user=request.user,saler=Product.objects.filter(product_id=int(new_prod)).first().shop,products=product1,size=prod_size).save()
				if int(new_prod) in trends:
				    t = trend.objects.filter(product = Product.objects.filter(product_id=int(new_prod)).first())[0]
				    t.number += 1
				    t.save()
				else:
				    trend(product = Product.objects.filter(product_id=int(new_prod)).first(), number=1).save()
				return redirect('/myorders')
			else:
				o_id = ''
				if Orders.objects.all().last():
					order_id = 'ordr'+str((Orders.objects.all().last().pk)+1)
				else:
					order_id = 'ordr001'
				o_id = order_id
				product1 = new_prod+'|'+str(1)+','
				Orders(order_id=order_id,user=request.user,saler=Product.objects.filter(product_id=int(new_prod)).first().shop,products=product1,size=prod_size).save()
				if int(new_prod) in trends:
				    t = trend.objects.filter(product = Product.objects.filter(product_id=int(new_prod)).first())[0]
				    t.number += 1
				    t.save()
				else:
				    trend(product = Product.objects.filter(product_id=int(new_prod)).first(), number=1).save()
				delev = 0.0
				subtotal = Product.objects.filter(product_id=int(new_prod)).first().price
				tax = subtotal*int(Product.objects.filter(product_id=int(new_prod)).first().gst)/100
	
				param_dict = {

		                'MID': 'YOUR_MID',
		                'ORDER_ID': str(o_id),
		                'TXN_AMOUNT': str(subtotal+tax+delev),
		                'CUST_ID': request.user.username,
		                'INDUSTRY_TYPE_ID': 'Retail',
		                'WEBSITE': 'WEBSTAGING',
		                'CHANNEL_ID': 'WEB',
		                'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',

		        }
				param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
				return render(request, 'main/paytm.html', {'param_dict': param_dict})

	else:
		address_form = UserAddressForm(instance=request.user.userdetail)
		u_form2 = UserAddressForm1(instance=request.user)
	delev = 0.0
	subtotal = Product.objects.filter(product_id=int(new_prod)).first().price
	tax = subtotal*int(Product.objects.filter(product_id=int(new_prod)).first().gst)/100
	totl = round(subtotal+tax+delev, 2)
	params = {
			'allProds':allProds,
			'cart_element_no' : len([p for p in Cart.objects.all() if p.user == request.user]),
			'address_form': address_form,
			'u_form':u_form2,
			'total':totl,
			'category':category.objects.all(),
		}
	return render(request, 'main/checkout2.html', params)

@login_required
def checkout(request):
	temp = 0
	allProds = []
	cart_prods = [p for p in Cart.objects.all() if p.user == request.user]
	for cprod in cart_prods:
		prod = Product.objects.filter(product_id=cprod.product_id)[0]
		allProds.append([cprod, prod])
	if request.method == 'POST':
		address_form = UserAddressForm(request.POST, instance=request.user.userdetail)
		u_form2 = UserAddressForm1(request.POST, instance=request.user)
		if address_form.is_valid() and u_form2.is_valid():
			address_form.save()
			u_form2.save()
			pay_mode = request.POST.get('pay_mode')
			trends = [i.product.product_id for i in trend.objects.all()]
# 			print(order)
			if pay_mode == 'on':
				for item in cart_prods:
					if Orders.objects.all().last():
						order_id = 'ordr'+str((Orders.objects.all().last().pk)+1)
					else:
						order_id = 'ordr001'
					product1 = item.product_id+'|'+str(item.number)+','
					Orders(order_id=order_id,user=request.user,saler=Product.objects.filter(product_id=int(item.product_id)).first().shop,products=product1, size=item.product_size).save()
					item.delete()
					if int(item.product_id) in trends:
					    t = trend.objects.filter(product = Product.objects.filter(product_id=int(item.product_id)).first())[0]
					    t.number += 1
					    t.save()
					else:
					    trend(product = Product.objects.filter(product_id=int(item.product_id)).first(), number=1).save()
				return redirect('/myorders')
			else:
				temp = 1
	else:
		address_form = UserAddressForm(instance=request.user.userdetail)
		u_form2 = UserAddressForm1(instance=request.user)
	subtotal = 0.0
	delev = 0.0
	tax = 0.0
	for p in cart_prods:
		tempTotal = p.number * Product.objects.filter(product_id=p.product_id)[0].price
		subtotal += tempTotal
		tax += tempTotal*int(Product.objects.filter(product_id=p.product_id).first().gst)/100

	if temp == 1:
		o_id = ''
		for item in cart_prods:
			order_id = 'ordr'+str((Orders.objects.all().last().pk)+1)
			o_id = order_id
			product1 = item.product_id+'|'+str(item.number)+','
			Orders(order_id=order_id,user=request.user,saler=Product.objects.filter(product_id=int(item.product_id)).first().shop,products=product1, size=item.product_size)
			
			if int(item.product_id) in trends:
			    t = trend.objects.filter(product = Product.objects.filter(product_id=int(item.product_id)).first())[0]
			    t.number += 1
			    t.save()
			else:
			    trend(product = Product.objects.filter(product_id=int(item.product_id)).first(), number=1)
		param_dict = {

                'MID': 'YOUR_MID',
                'ORDER_ID': str(o_id),
                'TXN_AMOUNT': str(subtotal+tax+delev),
                'CUST_ID': request.user.username,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',

        }
		param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
		return render(request, 'main/paytm.html', {'param_dict': param_dict})

	params = {
			'allProds':allProds,
			'cart_element_no' : len(cart_prods),
			'address_form': address_form,
			'u_form':u_form2,
			'total':subtotal+tax+delev,
			'category':category.objects.all(),
		}
	return render(request, 'main/checkout.html', params)

@csrf_exempt
def handlerequest(request):
	cart_prods = [p for p in Cart.objects.all() if p.user == request.user]
    # paytm will send you post request here
	form = request.POST
	response_dict = {}
	for i in form.keys():
		response_dict[i] = form[i]
		if i == 'CHECKSUMHASH':
			checksum = form[i]

	verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
	if verify:
		if response_dict['RESPCODE'] == '01':
			for item in cart_prods:
				order_id = 'ordr'+str((Orders.objects.all().last().pk)+1)
				o_id = order_id
				product1 = item.product_id+'|'+str(item.number)+','
				Orders(order_id=order_id,user=request.user,saler=Product.objects.filter(product_id=int(item.product_id)).first().shop,products=product1, size=item.product_size).save()
				item.delete()
				if int(item.product_id) in trends:
				    t = trend.objects.filter(product = Product.objects.filter(product_id=int(item.product_id)).first())[0]
				    t.number += 1
				    t.save()
				else:
					trend(product = Product.objects.filter(product_id=int(item.product_id)).first(), number=1).save()
			print('order successful')
		else:
			print('order was not successful because' + response_dict['RESPMSG'])
	return render(request, 'main/paymentstatus.html', {'response': response_dict})

def MyOrders(request):
	if request.method == 'POST':
		order_id = request.POST.get('order_id')
		o = Orders.objects.filter(order_id=order_id)[0]
		o.status = 'Cancel'
		o.save()
	params = {
		'orders': [i for i in Orders.objects.all() if i.user == request.user and i.status != 'Delivered' and i.status != 'Cancel'],
		'delivered': [i for i in Orders.objects.all() if i.user == request.user and i.status == 'Delivered'],
		'cancel': [i for i in Orders.objects.all() if i.user == request.user and i.status == 'Cancel'],

	}
	return render(request,'main/myorders.html', params)

def MenuFilter(request, querys):
	print(querys.split(',')[0])
	prod = []
	for p in [i for i in Product.objects.all() if str(i.category).lower() == querys.split(',')[0].lower() and str(i.subcategory).lower()==querys.split(',')[1].lower()]:
		prod.append([p,[item for item in ProductSize.objects.filter(product=p)]])
	params = {
		'product':prod,
		'catg':querys,
		'cart_element_no' : len([p for p in Cart.objects.all() if p.user == request.user]),
		'category':category.objects.all(),
		}
	return render(request, 'main/view_all.html', params)

def contact(request):
	if request.method == 'POST':
		cont_name = request.POST.get('Name', default='')
		cont_email = request.POST.get('Email', default='')
		cont_subject = request.POST.get('Subject', default='')
		cont_mess = request.POST.get('Message', default='')
		con = Contact(name = cont_name, email = cont_email, subject = cont_subject, message = cont_mess)
		con.save()
		messages.success(request, 'Your message has been sent. Thank you!')

	return render(request, 'main/contact.html', {'category':category.objects.all(),'cart_element_no' : len([p for p in Cart.objects.all() if p.user == request.user]),})