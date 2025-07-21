from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from users.models import User
from .filters import User,UserFilter

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
    
class ListUser(LoginRequiredMixin,View):
    login_url='login_admin_url'
    template_name = "admin/user_list.html"
    def get(self,request):
      
        my_users= User.objects.exclude(is_superuser=1).order_by('-created_at').values('email','phone_number','is_active','username','id',"created_at")
        
        user_filter=UserFilter(request.GET,queryset=my_users)
        
        # users = User.objects.exclude(is_superuser=1).values('email','phone_number','is_active','username','id')
        
        return render(request,self.template_name,{"users":user_filter.qs,'myFilter':user_filter})

class UserDetails(LoginRequiredMixin,View):
    template_name="admin/customer_details.html"
    def get(self,request,id):
        user = User.objects.get(id=id)
        return render(request,self.template_name,{'user':user})
    


    