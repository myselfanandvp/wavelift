from .forms import SignupForm, LoginForm, Change_Password_Form, OTPVerificationForm, ResetPasswordForm, Admin_Login_Form
from random import randint
from .models import User
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from datetime import datetime


# OTP generator helper
def generate_and_send_otp(**kwargs):
    otp = randint(100000, 999999)
    request = kwargs['request']
    request.session['otp'] = otp
    request.session['otp_created_at'] = datetime.now().isoformat()
    request.session.set_expiry(300)  # Enforce 5-minute expiry

    # Compose email
    subject = "Your One-Time Password for Password Reset"
    message = f"""
    Dear {request.session.get('user_name')},

        Your one-time password (OTP) is: {otp}

        Please use this code to complete your password reset. This code is valid for 5 minutes.

        If you did not request this, please ignore this message.

        Best regards,
        WaveLift Support Team

    """

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [request.session.get('user_email')],
        fail_silently=False
    )


def get_session_user(request):
    email = request.session.get('user_email')
    if not email:
        return None
    return User.objects.filter(email=email).first()


# Create your views here.


# User Views

@method_decorator(never_cache, name='dispatch')
class LoginUser(View):
    template_name = "user/user_login_page.html"
    admin_template_name = ""

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email, password = form.cleaned_data.get(
                'email'), form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(user=user, request=request)
                if request.user.is_superuser:
                    return redirect('admin_dashboard_url')
                return redirect("index_page")
            else:
                form.add_error("password", "Password or email is wrong")

        return render(request, self.template_name, {"form": form})


@method_decorator(never_cache, name='dispatch')
class SignupUser(View):
    template_name = 'user/user_signup_page.html'

    def get(self, request):
        form = SignupForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_user_url')
        return render(request, self.template_name, {"form": form})


@method_decorator(never_cache, name='dispatch')
class LogoutUser(LoginRequiredMixin,View):
    def post(self, request):
        is_admin = request.user.is_superuser  # Store the flag before logout
        logout(request)
        messages.success(request, "Logged out successfully")
        if is_admin:
            return redirect("login_admin_url")        
        return redirect("login_user_url")


@method_decorator(never_cache, name='dispatch')
class ChangePassword(View):
    template_name = 'user/change_password.html'

    def get(self, request):

        if not request.session.get('user_email'):
            return redirect('forgot_password_url')  # or your OTP page
        form = Change_Password_Form()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = Change_Password_Form(request.POST)
        if form.is_valid():
            password, confirm_password = form.cleaned_data['password1'], form.cleaned_data['password2']
            if password == confirm_password and (password is not None and confirm_password is not None):
                user = get_session_user(request)
                user.set_password(form.cleaned_data['password1'])
                user.save()
                messages.success(
                    request, "Your password has been updated successfully.")
                if user.is_superuser:
                    request.session.pop('user_email', None)
                    request.session.pop('user_name', None)
                    return redirect("login_admin_url")
                else:
                    return redirect("login_user_url")

            form.add_error("password2", "Passwords do not match.")

        return render(request, self.template_name, {"form": form})


@method_decorator(never_cache, name='dispatch')
class OTP_Validation(View):
    template_name = 'user/otp_validation.html'

    def get(self, request):
        if not request.session.get('user_email'):
            return redirect('forgot_password_url')  # or your OTP page
        
        form = OTPVerificationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            try:
                otp_input = int(form.get_otp())
            except (ValueError, TypeError):
                form.add_error(None, "Invalid OTP format.")
                return render(request, self.template_name, {'form': form})

            session_otp = request.session.get('otp')
            otp_create_at = request.session.get('otp_created_at')

            if not session_otp or not otp_create_at:
                form.add_error(
                    None, "OTP session expired. Please request a new one.")
                return render(request, self.template_name, {'form': form})
            otp_time = datetime.fromisoformat(otp_create_at)
            if (datetime.now() - otp_time).total_seconds() > 300:
                form.add_error(
                    None, "OTP has expired. Please request a new one.")
                return render(request, self.template_name, {"form": form})

            attempts = request.session.get('otp_attempts', 0)

            if attempts >= 5:
                form.add_error(
                    None, "Too many attempts. Please request a new OTP.")
                return render(request, self.template_name, {"form": form})

            if int(session_otp) == otp_input:
                request.session.pop('otp', None)
                request.session.pop('otp_created_at', None)
                request.session.pop('otp_attempts', None)
                return redirect('change_password_url')
            else:
                request.session['otp_attempts'] = attempts + 1
                form.add_error(None, "Entered otp is wrong")
        return render(request, self.template_name, {'form': form})


@method_decorator(never_cache, name='dispatch')
class ForgotPassword(View):
    template_name = 'user/reset_password_email.html'

    def get(self, request):
        form = ResetPasswordForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(
                email=form.cleaned_data['email']).first()
            if user is not None:
                request.session['user_email'] = user.email
                request.session['user_name'] = user.username
                request.session.set_expiry(300)
                generate_and_send_otp(request=request)
                messages.success(request, "OTP has been sent to your email.")
                return redirect('otp_validation_url')

            form.add_error("email", "Email you are given is wrong")

        return render(request, self.template_name, {"form": form})


@method_decorator(never_cache, name='dispatch')
class ResendOTP(View):
    def post(self, request):
        request.session.pop('otp_attempts', None)  # Reset failed attempts
        generate_and_send_otp(request=request)
        return JsonResponse({'status': 'success', 'message': 'OTP resent successfully!'})


# Admin Views
@method_decorator(never_cache, name='dispatch')
class LoginAdmin(View):
    template_name = 'admin/admin_login.html'

    def get(self, request):
        form = Admin_Login_Form()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = Admin_Login_Form(request.POST)
        if form.is_valid():
            email, password = form.cleaned_data.get(
                'email'), form.cleaned_data.get('password')
            print(password, email)
            admin = authenticate(request, username=email, password=password)
            if admin is not None:
                login(request, admin)
                return redirect('admin_dashboard_url')
            form.add_error("password", "Username or Password is wrong!")
        return render(request, self.template_name, {"form": form})
