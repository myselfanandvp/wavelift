from django.shortcuts import render,redirect,get_object_or_404
from .forms import ProductForm, ProductImagesForm, ProductCategoryForm,CreatColorForm,ProductColor
from .models import Category
from django.views import View
from django.http import HttpResponse,HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product,ProductImage
from .filters import ProductFilter,CategoryFilter
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
# Create your views here.

def check_permission(**kwargs):
    request = kwargs.get('request')
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to access this page.")


# Product Views
@method_decorator(never_cache, name='dispatch')
class CreateProudctView(LoginRequiredMixin,View):
    login_url="login_admin_url"
    template_name = "products/create_product.html"
    def get(self, request):
        premission=check_permission(request=request)
        if premission:
            return premission
        
        form = ProductForm()
        product_images = ProductImagesForm()

        return render(request, self.template_name, {"form": form,"product_images_form":product_images})
    

    def post(self, request):        
        form = ProductForm(request.POST)
        product_images_form = ProductImagesForm(request.POST, request.FILES)
        if product_images_form.is_valid() and form.is_valid():
            product= form.save(commit=False)
            product.save()
            # Handle colors as a single Color instance or None
            product.colors.set(form.cleaned_data['colors'])
            images=product_images_form.cleaned_data.get('images',[])
            for index,image in enumerate(images):
                product_image=ProductImage(
                    product=product,
                    image=image,
                    is_primary=(index==0),
                )
                product_image.save()
            return redirect("list_products_url")          
                
        return render(request, self.template_name, {"form": form,"product_images_form":product_images_form})
     
    
@method_decorator(never_cache, name='dispatch')
class ListProductView(LoginRequiredMixin,View):
    template_name="products/list_products.html"
    def get(self,request):
        premission=check_permission(request=request)
        if premission:
            return premission
        products = Product.objects.all()
        filter = ProductFilter(request.GET,queryset=products)   
        page_number = request.GET.get('page')  # Use 'page' as the query parameter
        paginator = Paginator(filter.qs, per_page=3)
        page_obj = paginator.get_page(page_number)  # Get the page object
     
        return render(request,self.template_name,{'products':filter.qs,"myFilter":filter,"pages":page_obj})
        
    def post(self,request):
        pass



@method_decorator(never_cache, name='dispatch')
class EditProductView(LoginRequiredMixin, View):
    login_url = "login_admin_url"
    # template_name = "products/edit_product.html"  
    template_name = "products/edit_product.html"  

    def get(self, request, product_id):
        # Check permissions
        permission = check_permission(request=request)
        if permission:
            return permission

        # Get the existing product
        product = get_object_or_404(Product, id=product_id)
        # Populate forms with existing data
        form = ProductForm(instance=product)
        product_images_form = ProductImagesForm()
        existing_images = Product.objects.prefetch_related("images").filter(id=product_id)
        return render(request, self.template_name, {
            "form": form,
            "product_images_form": product_images_form,
            "product": product,
            "existing_products":existing_images
        })

    def post(self, request, product_id):
        # Get the existing product
        product = get_object_or_404(Product, id=product_id)
        # Initialize forms with POST data and instance
        form = ProductForm(request.POST, instance=product)
        product_images_form = ProductImagesForm(request.POST, request.FILES)

        if product_images_form.is_valid() and form.is_valid():
            # Save updated product details
            form.save()

            # Handle images
            images = product_images_form.cleaned_data.get('images', [])
            if images:  # Only update images if new ones are provided
                # Optionally, delete existing images (uncomment if needed)
                # ProductImage.objects.filter(product=product).delete()
                for index, image in enumerate(images):
                    product_image = ProductImage(
                        product=product,
                        image=image,
                        is_primary=(index == 0),
                    )
                    product_image.save()

            return redirect("list_products_url")

        return render(request, self.template_name, {
            "form": form,
            "product_images_form": product_images_form,
            "product": product
        })

# Category Views
@method_decorator(never_cache, name='dispatch')
class CreateCategory(LoginRequiredMixin,View):
    template_name = "products/create_category.html"

    def get(self, request):
        premission=check_permission(request=request)
        if premission:
            return premission
        form = ProductCategoryForm()
        return render(request,self.template_name,{"form":form,'iscreate':True})      

    def post(self, request):
        form = ProductCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_category_url")
        form.add_error(None,"Category is not saved")
        return render(request,self.template_name,{"form":form,'iscreate':True})
    
@method_decorator(never_cache, name='dispatch') 
class ListCategory(LoginRequiredMixin,View):
    template_name = 'products/list_category.html'
    def get(self,request):
        premission=check_permission(request=request)
        if premission:
            return premission
        
        categorys = Category.objects.all().order_by("-created_at")
        page_number = request.GET.get('page')  # Use 'page' as the query parameter
        filter = CategoryFilter(request.GET,queryset=categorys) 
        paginator = Paginator(filter.qs, per_page=10)
        page_obj = paginator.get_page(page_number)  # Get the page object
        return render(request,self.template_name,{'categorys':filter.qs,'filter':filter,"pages":page_obj})
        
   
@method_decorator(never_cache, name='dispatch')
class EditCategory(LoginRequiredMixin,View):
    template_name = "products/create_category.html"
    def get(self, request,id):
        premission=check_permission(request=request)
        if premission:
            return premission
        category = get_object_or_404(Category,id=id)
        form = ProductCategoryForm(instance=category)
        return render(request,self.template_name,{'form':form})

    def post(self, request,id):
        permission = check_permission(request=request)
        if permission:
            return permission
        category = get_object_or_404(Category, id=id)
        form = ProductCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('list_category_url')
        return render(request, self.template_name, {'form': form})

@method_decorator(never_cache, name='dispatch')
# Soft delete on category
class DeleteCategory(LoginRequiredMixin,View):   
    def post(self, request,id):
        premission=check_permission(request=request)
        if premission:
            return premission
        category_delete= Category.objects.filter(id=id).first()         
        if category_delete.status == 0:
            category_delete.status = 1
        else:
            category_delete.status = 0         
        category_delete.save(update_fields=['status'])
        return redirect("list_category_url")

    
class CreateColor(View):
    template_name="products/create_color.html"
    def get(self,request):
        form = CreatColorForm()
        colors = ProductColor.objects.all()
        return render(request,self.template_name,{'form':form,'colors':colors})
    
    def post(self,request):
        form = CreatColorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data.get('color')
            print(data)
            return HttpResponse("Color is saved")
        return HttpResponse("Color is notsaved")
        