from django.shortcuts import render
from .forms import ProductForm,ProductBrandForm,ProductImagesForm,ProductCategoryForm,ProductReviewForm
from django.views import View
# Create your views here.


class CreateProudctView(View):
    template_name ="products/create_product.html"
    def get(self,request):
        form = ProductForm()
        product_images = ProductImagesForm()
        
        return render(request,self.template_name,{"form":form})
    
    def post(self,request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            
            
