"""crm_main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from apps.common import views
from apps.common.views import HomeView, SignUpView, DashboardView, ProfileUpdateView, ProfileView, ChartView, \
    OrderListView, AboutView, ClientsView, SuppliersListView, TasksView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('profile-update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('tasks/', views.tasks, name='tasks'),
    path('check_order/<int:order_id>/', views.check_order, name='check_order'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('about/', AboutView.as_view(), name='about'),
    path('suppliers/', views.suppliers_list, name='suppliers'),
    path('clients/', views.clients, name='clients'),
    path('client_profile_update/<int:client_id>/', views.client_profile_update, name='client_profile_update'),
    path('clientprofile/<int:client_id>/', views.client_profile, name='client_profile'),
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='common/login.html'),
        name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='home'),
        name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('change-password',
         auth_views.PasswordChangeView.as_view(
             template_name='common/change-password.html',
             success_url='/'
         ),
         name='change-password'),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='common/password-reset/password_reset.html',
             subject_template_name='common/password-reset/password_reset_subject.txt',
             email_template_name='common/password-reset/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='common/password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='common/password-reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='common/password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('charts/', ChartView.as_view(template_name='common/charts.html'), name='charts'),
    path('tables/', OrderListView.as_view(template_name ='common/tables.html'), name='tables'),
    path('newproduct/', views.new_product, name='new_product'),

    #path('graph/', home, name='home'),
    path('pie-chart/', views.pie_chart, name='pie-chart'),
    path('cart/', include('apps.cart.urls'), name='cart'),
    path('shop/', include('apps.shop.urls'), name='shop'),
    path('orders/', include('apps.orders.urls'), name='orders'),
    path('payment/', include('apps.payment.urls'), name='payment'),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    path('products/', views.product, name='products'),
    path('productsWare/', views.product_list, name='productsWare'),
    url(r'^remove/(?P<product_id>\d+)/$', views.remove_it, name='remove_it'),
    url(r'^update/(?P<product_id>\d+)/$', views.update_prod, name='update_prod'),
    path('change_status/<int:order_id>', views.change_status, name='change_status'),
    path('order_statictic/', views.get_last_month_statistic, name='order_statistic'),

    path('newsupplier/', views.new_supplier, name='newsupplier'),
    path('testclient/', views.add_client, name = 'testclient')
    #path('newproduct/', views.
    #url(r'^$', views.cart_detail, name='cart_detail'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
