from django.shortcuts import render
from django.views import View

# Create your views here.

class  HomePage(View):
    template_name= 'core/index.html'
    def get(self,request):
        return render(request,self.template_name,{})
    
class Contactus(View):
    template_name = 'core/contact.html'
    def get(self,request):
        return render(request,self.template_name,{})
    
class Aboutus(View):
    template_name='core/about.html'
    def get(self,request):
        return render(request,self.template_name,{})
