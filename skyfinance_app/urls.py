
from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView, PasswordChangeView

urlpatterns = [
    path('signup/', views.register_view, name = 'signup'),
    path('Login/', views.login_view, name = 'login'),
    path('overview/', views.overview_view, name = 'overview'),
    path('email_verification/', views.CustomPasswordResetView.as_view(), name = 'email_verification'),
    
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='skyfinance_app/password_reset_confirm.html'), 
         name='password_reset_confirm'),
         
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='skyfinance_app/password_reset_complete.html'), 
         name='password_reset_complete'),
     
     path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

     path('add_transaction/', views.add_transaction_view, name = 'add_transaction'),
     path('edit_transaction/<int:pk>/', views.edit_transaction_view, name = 'edit_transaction'),
     path('delete_transaction/<int:pk>/', views.delete_transaction_view, name = 'delete_transaction'),
     path('dashboard/', views.dashboard_view, name = 'dashboard'),
     path('settings/', views.settings_view, name = 'settings'),
     path('password_change/', PasswordChangeView.as_view(template_name = 'skyfinance_app/password_change.html',
                                                        success_url = reverse_lazy('dashboard')), name = 'password_change'),
]