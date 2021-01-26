from django.urls import path, reverse_lazy
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from blogs import settings
from account import views as account_views
from account import forms as account_forms

app_name = 'account'

urlpatterns = [
    # path('orders/<int:id>', account_views.order_details, name='order_details'),
    # path('orders/', account_views.orders_view, name='orders_list'),
    # path('profile/', account_views.profile, name='profile'),
    # path('wishlist/', account_views.wishlist_view, name='wishlist'),

    path('register/', account_views.register_view, name='register'),
    path('login/', account_views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='articles:index'), name='logout'),

    path('change-password/',
         auth_views.PasswordChangeView.as_view(
             template_name='account/change-password.html',
             success_url='/',
         ), name='change_password'),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='account/password-reset/password_reset.html',
             form_class=account_forms.CustomPasswordResetForm,
             email_template_name='account/password-reset/password_reset_email.html',
             success_url=reverse_lazy('account:password_reset_done',)
         ), name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='account/password-reset/password_reset_done.html'
         ), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='account/password-reset/password_reset_confirm.html',
             success_url=reverse_lazy('account:password_reset_complete')
         ), name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='account/password-reset/password_reset_complete.html',
         ), name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
