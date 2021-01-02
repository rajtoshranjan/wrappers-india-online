from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from saler.views import admin2

urlpatterns = [
    path('wrappers/india/my/admin/pannel/home/', admin.site.urls),
    path('wrappers/india/my/admin/pannel/admin20/', admin2, name = 'admin2'),
    path('', include('main.urls')),
    path('seller/', include('saler.urls')),
    path("login/", auth_views.LoginView.as_view(template_name='main/login.html', redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page='login'), name="logout"),
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name='main/password_reset.html'), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='main/password_reset_done.html'), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='main/password_reset_confirm.html'), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name='main/password_reset_complete.html'), name="password_reset_complete"),
    path("coupon/",include('coupon.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
