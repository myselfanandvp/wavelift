from django.shortcuts import render
from .forms import ProductForm, ProductBrandForm, ProductImagesForm, ProductCategoryForm, ProductReviewForm
from django.views import View
from django.http import HttpResponse,HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def check_permission(**kwargs):
    request = kwargs.get('request')
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to access this page.")




class CreateProudctView(View):
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
        return HttpResponse(f"Product created {form.cleaned_data.get("name")}")


"""
Category crud operations
"""


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
