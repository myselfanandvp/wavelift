from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from users.models import User
from .filters import User,UserFilter
from django.core.paginator import Paginator

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
        page_number = request.GET.get('page')  # Use 'page' as the query parameter
        paginator = Paginator(user_filter.qs, per_page=3)
        page_obj = paginator.get_page(page_number)  # Get the page object
     
        return render(request,self.template_name,{"users":user_filter.qs,'myFilter':user_filter,'pages':page_obj})

class UserDetails(LoginRequiredMixin,View):
    template_name="admin/customer_details.html"
    def get(self,request,id):
        user = User.objects.get(id=id)
        return render(request,self.template_name,{'user':user})
    


    