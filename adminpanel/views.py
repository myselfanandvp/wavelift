from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
# Create your views here.

@method_decorator(never_cache, name='dispatch')
class AdminDashboard(LoginRequiredMixin,UserPassesTestMixin,View):
    login_url='login_admin_url'
    template_name = 'admin/admin_dashboard.html'
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        return redirect(self.login_url)
    
    def get(self,request):
        return render(request,self.template_name,{})
    
    
    def post(self,request):
        pass
    
    
@method_decorator(never_cache, name='dispatch')
class ListProducts(LoginRequiredMixin,View):
    login_url= 'login_admin_url'
    template_name="admin/product_list.html"
    def get(self,request):
        return render(request,self.template_name,{})
    def post(self,request):
        pass