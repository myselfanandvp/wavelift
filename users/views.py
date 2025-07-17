from .forms import UserForm, LoginForm, Admin_Login_Form, Change_Password_Form, OTPVerificationForm, RestPassword
from random import randint
from .models import User
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings





def generate_and_send_otp(**kwargs):
    otp = randint(100000, 999999)
    # Compose email
    subject = "Your One-Time Password for Password Reset"
    message = f"""
    Dear {kwargs['request'].session['user_name']},

        Your one-time password (OTP) is: {otp}

        Please use this code to complete your password reset. This code is valid for 10 minutes.

        If you did not request this, please ignore this message.

        Best regards,
        WaveLift Support Team

    """
    kwargs['request'].session['otp']=otp
    send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [kwargs['request'].session['user_email']],
                fail_silently=False
            )
   



# Create your views here.


class LoginUser(View):
    template_name = "user/user_login_page.html"

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
                return redirect("index_page")
            else:
                form.add_error("password", "Password or email is wrong")

        return render(request, self.template_name, {"form": form})


class SignupUser(View):
    template_name = 'user/user_signup_page.html'

    def get(self, request):
        form = UserForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_user_url')
        return render(request, self.template_name, {"form": form})


class LogoutUser(View):
    def post(self, request):
        logout(request)
        return redirect("login_user_url")


class ChangePassword(View):
    template_name = 'user/change_password.html'

    def get(self, request):
        return render(request, self.template_name, {"form": Change_Password_Form})

    def post(self, request):
        pass


class OTP_Validation(View):
    template_name = 'user/otp_validation.html'

    def get(self, request):
        form = OTPVerificationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            if request.session['otp'] == form.get_otp():
                print(request.session['otp'])
                return redirect('change_password_url')
            form.add_error(None, "Entered otp is wrong")
        return render(request,self.template_name,{'form':form})


class ForgotPassword(View):
    template_name = 'user/reset_password_email.html'

    def get(self, request):
        form = RestPassword()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = RestPassword(request.POST)
        if form.is_valid():
            user = User.objects.filter(
                email=form.cleaned_data['email']).first()
            if user is not None:
                request.session['user_email']=user.email
                request.session['user_name']=user.username
                generate_and_send_otp(request=request)
                return redirect('otp_validation_url')

            form.add_error("email", "Email you are given is wrong")

        return render(request, self.template_name, {"form": form})


class ResendOTP(View):
    def post(self, request):
        generate_and_send_otp(request=request)
        return JsonResponse({'status': 'success', 'message': 'OTP resent successfully!'})


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


class LogoutAdmin(View):
    def get(self, request):
        pass

    def post(self, request):
        pass
