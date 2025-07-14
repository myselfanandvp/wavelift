from .forms import User,UserForm,LoginForm,Admin_Login_Form,Change_Password_Form,OTPVerificationForm,RestPassword
from django.shortcuts import render
from django.views import View

# Create your views here.

class LoginUser(View):
    template_name = "user/user_login_page.html"
    def get(self,request):
        return render(request,self.template_name,{'form':LoginForm})
    def post(self,request):
        pass
    
class SignupUser(View):
    template_name= 'user/user_signup_page.html'
    def get(self,request):
        form = UserForm()
        return render(request,self.template_name,{'form':form})
    def post(self,request):
        pass
    
class LogoutUser(View):
    def get(self,request):
        pass
    def post(self,request):
        pass
    
class ChangePassword(View):
    template_name='user/change_password.html'
    def get(self,request):
        return render(request,self.template_name,{"form":Change_Password_Form})
    def post(self,request):
        pass
    
class OTP_Validation(View):
    template_name='user/otp_validation.html'
    def get(self,request):
        return render(request,self.template_name,{"form":OTPVerificationForm})
    def post(self,request):
        pass
    
class ForgotPassword(View):
    template_name='user/reset_password_email.html'
    
    def get(self,request):
        return render(request,self.template_name,{"form":RestPassword})
    def post(self,request):
        pass

class LoginAdmin(View):
    template_name='admin/admin_login.html'
    def get(self,request):
        return render(request,self.template_name,{"form":Admin_Login_Form})
    def post(self,request):
        pass


class LogoutAdmin(View):
    def get(self,request):
        pass 
    
    def post(self,request):
        pass