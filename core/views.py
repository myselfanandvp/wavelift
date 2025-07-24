from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from products.models import Product
# Create your views here.


class  HomePage(View):
    template_name= 'core/index.html'

    def get(self,request):
        if request.user.is_superuser:
            return redirect("admin_dashboard_url")
        products = Product.objects.all()
        new_arrivals = Product.objects.select_related('category').filter(category__name__istartswith="New Arrival")

        return render(request,self.template_name,{'products':products,'new_arrivals':new_arrivals})
    
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
    
    
class AllProducts(View):
    template_name= "core/all_products.html"
    def get(self,request):
        products = Product.objects.all()
        return render(request,self.template_name,{'products':products})
    

