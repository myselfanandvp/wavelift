from .views import SignupUser,LoginUser,LoginAdmin,ChangePassword,OTP_Validation,ForgotPassword
from django.urls import path
urlpatterns=[
    path('signup/',SignupUser.as_view(),name="signup_user_url"),
    path('login/',LoginUser.as_view(),name="login_user_url"),
    path('admin_login/',LoginAdmin.as_view(),name="login_admin_url"),
    path('change_password/',ChangePassword.as_view(),name="change_password_url"),
    path('otp_validation/',OTP_Validation.as_view(),name="otp_validation_url"),
    path('forgot_password/',ForgotPassword.as_view(),name="forgot_password_url"),
]