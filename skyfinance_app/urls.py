
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signup/', views.register_view, name = 'signup'),
    path('Login/', views.login_view, name = 'login'),
    path('overview/', views.overview_view, name = 'overview'),
    path('Email_verification', views.CustomPasswordResetView.as_view(), name = 'email_verification'),
    
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='skyfinance_app/password_reset_confirm.html'), 
         name='password_reset_confirm'),
         
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='skyfinance_app/password_reset_complete.html'), 
         name='password_reset_complete'),
     
     path('logout/', LogoutView.as_view(next_page='login'), name='logout')
]