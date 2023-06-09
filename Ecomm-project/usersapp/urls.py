from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('confirm-registration/<str:encoded_pk>/<str:token>/',
         views.ConfirmRegistrationView.as_view(), name='confirm-register'),
    path('change_password/', views.ChangePasswordView.as_view(),
         name='change_password'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password-reset/', views.ResetPasswordView.as_view(), name='reset-password'),
    path('password-reset/<str:encoded_pk>/<str:token>/',
         views.PasswordResetConfirmView.as_view(), name='reset-password'),
    path('account-delete/', views.DeleteUserView.as_view(), name='delete-account'),

    # customer views
    path('customers/', views.CustomerView.as_view(), name='customers'),
    path('sellers/', views.SellerView.as_view(), name='sellers'),

    # address views
    path('address/', views.AddressView.as_view(), name='address'),


    # admin api's
    path('admin-update/', views.AdminView.as_view(), name='admin-update'),
    path('admin-register/', views.AdminRegisterView.as_view(), name='admi-register'),
    path('product-activation-status/',
         views.ProductActivation.as_view(), name='product-activation'),

]
