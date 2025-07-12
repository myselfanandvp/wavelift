from django.shortcuts import render
from django.views import View
from .forms import User,UserForm

# Create your views here.

class LoginUser(View):
    def get(self,request):
        pass
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

class LoginAdmin(View):
    def get(self,request):
        pass
    def post(self,request):
        pass


class LogoutAdmin(View):
    def get(self,request):
        pass 
    
    def post(self,request):
        pass