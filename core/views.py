from django.shortcuts import render,redirect
from django.views import View

# Create your views here.

class  HomePage(View):
    template_name= 'core/index.html'

    def get(self,request):
        if request.user.is_superuser:
            return redirect("admin_dashboard_url")
        return render(request,self.template_name,{})
    
class Contactus(View):
    template_name = 'core/contact.html'
    def get(self,request):
        return render(request,self.template_name,{})
    
class Aboutus(View):
    template_name='core/about.html'
    def get(self,request):
        return render(request,self.template_name,{})
    
    
class Term_And_Condition(View):
    template_name="core/terms-and-condition.html"
    def get (self,request):
        return render(request,self.template_name,{})
    
class Policy(View):
    template_name = "core/privacy_policy.html"
    def get (self,request):
        return render(request,self.template_name,{})
    
    
class PageNotFound(View):
    template_name = "shared/page_notfound.html"
    
    def get(self,request):
        return render(request,self.template_name,{})
    

