from django.urls import path,include
from . import views

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name='register'),
    path('confirm-registration/<str:encoded_pk>/<str:token>/',views.ConfirmRegistrationView.as_view(),name='confirm-register'),
    path('change_password/',views.ChangePasswordView.as_view(),name='change_password'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('password-reset/',views.ResetPasswordView.as_view(),name='reset-password'),
    path('password-reset/<str:encoded_pk>/<str:token>/',views.PasswordResetConfirmView.as_view(),name='reset-password'),
]