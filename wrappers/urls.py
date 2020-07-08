"""wrappers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('wrappers/india/my/admin/pannel/home/', admin.site.urls),
    path('', include('main.urls')),
    path('seller/', include('saler.urls')),
    path("login/", auth_views.LoginView.as_view(template_name='main/login.html', redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page='login'), name="logout"),
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name='main/password_reset.html'), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='main/password_reset_done.html'), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='main/password_reset_confirm.html'), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name='main/password_reset_complete.html'), name="password_reset_complete"),
    path("coupon/",include('coupon.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
