from django.shortcuts import render,redirect
from .forms import ProductForm, ProductBrandForm, ProductImagesForm, ProductCategoryForm, ProductReviewForm
from django.views import View
from django.http import HttpResponse,HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product
from .filters import ProductFilter
from django.core.paginator import Paginator
# Create your views here.

def check_permission(**kwargs):
    request = kwargs.get('request')
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to access this page.")


# Product Views

class CreateProudctView(LoginRequiredMixin,View):
    login_url="login_admin_url"
    template_name = "products/create_product.html"

    def get(self, request):
        premission=check_permission(request=request)
        if premission:
            return premission
        
        form = ProductForm()
        product_images = ProductImagesForm()

        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("list_products_url")
    
    
class ListProductView(View):
    template_name="products/list_products.html"
    def get(self,request):
        products = Product.objects.all()
        filter = ProductFilter(request.GET,queryset=products)   
        page_number = request.GET.get('page')  # Use 'page' as the query parameter
        paginator = Paginator(filter.qs, per_page=3)
        page_obj = paginator.get_page(page_number)  # Get the page object
     
        return render(request,self.template_name,{'products':filter.qs,"myFilter":filter,"pages":page_obj})
        
    def post(self,request):
        pass


# Category Views



class CreateCategory(LoginRequiredMixin,View):
    template_name = "products/create_category.html"

    def get(self, request):
        premission=check_permission(request=request)
        if premission:
            return premission
        form = ProductCategoryForm()
        return render(request,self.template_name,{"form":form})      

    def post(self, request):
        form = ProductCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Category was saved")
        form.add_error(None,"Category is not saved")
        return render(request,self.template_name,{"form":form})


class EditCategory(View):
    template_name = "products/edit_category.html"

    def get(self, request):
        pass

    def post(self, request):
        pass


# Soft delete on category
class DeleteCategory(View):
    def get(self, request):
        pass

    def post(self, request):
        pass
    
    
    
