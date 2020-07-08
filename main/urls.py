from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('register/', views.register, name="signup"),
    path('account_settings/', views.account_settings, name="account_settings"),
    path("product/<int:prod_id>", views.productView, name="ProductView"),
    path('contact/', views.contact, name="contact"),
    path("products/<str:catg>", views.view_all, name="products_view_all"),
    path('plus_element_cart/', views.plus_element_cart),
    path('minus_element_cart/', views.minus_element_cart),
    path('add_to_cart/', views.add_to_cart),
    path('delete_from_cart/', views.delete_from_cart),
    path('dummy_cart/', views.dummy_cart),
    path('cart/', views.cart, name="main_cart"),
    path('checkout/', views.checkout, name="main_checkout"),
    path('order_now/', views.order_now, name="order_now"),
    path('myorders/', views.MyOrders, name="myorders"),
    path('search/', views.search, name="search"),
    path('MenuFilter/<str:querys>', views.MenuFilter, name="MenuFilter"),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),
    ]