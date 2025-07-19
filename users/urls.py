from .views import SignupUser,LoginUser,ChangePassword,OTP_Validation,ForgotPassword,LogoutUser,ResendOTP,LoginAdmin
from django.urls import path
urlpatterns=[
    path('signup/',SignupUser.as_view(),name="signup_user_url"),
    path('login/',LoginUser.as_view(),name="login_user_url"),
    path('logout/',LogoutUser.as_view(),name="logout_user_url"),
    path('change-password/',ChangePassword.as_view(),name="change_password_url"),
    path('otp/',OTP_Validation.as_view(),name="otp_validation_url"),
    path('resendotp/',ResendOTP.as_view(),name="resendotp_url"),
    path('forgot-password/',ForgotPassword.as_view(),name="forgot_password_url"),    
    # Admin Urls
    path('admin/login/',LoginAdmin.as_view(),name="login_admin_url"),
    
]