from django import forms
from .models import Product,Brand,Category,ProductImage,ProductReview,Color
from django.core.validators import FileExtensionValidator

inputfield_style={"class":"bg-gray-50 border border-gray-500 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"}
imagefield_style={"class":"hidden"}


class ProductForm(forms.ModelForm): 
    description=forms.CharField(widget=forms.Textarea(attrs={'class':"block w-full h-20 resize-none text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500"}))
    name = forms.CharField(widget=forms.TextInput(attrs={**inputfield_style}))
    slug = forms.CharField(widget=forms.TextInput(attrs={**inputfield_style}))
    price = forms.CharField(widget=forms.NumberInput(attrs={**inputfield_style}))
   
    category=forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select Category",
        required=True,
        widget=forms.Select(attrs={
            "class":"w-full px-3 py-2 text-sm text-gray-700 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:text-gray-200 dark:bg-gray-800 dark:border-gray-600 dark:focus:ring-blue-600"
        })
    )
    
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(),
        empty_label="Select Brand",
        required=True,
        widget=forms.Select(attrs={"class":"w-full px-3 py-2 text-sm text-gray-700 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:text-gray-200 dark:bg-gray-800 dark:border-gray-600 dark:focus:ring-blue-600"
                                   
                                   
                                   })
    )
    
    
    colors = forms.ModelMultipleChoiceField(
        queryset=Color.objects.all(),
        required=True,
        widget=forms.SelectMultiple(
            attrs={
                "class": "fg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
            }
        )
    )

    stock_qty= forms.CharField(widget=forms.NumberInput(attrs={**inputfield_style}))

    class Meta:
        model = Product
        # fields = ['description','name','brand','category','slug','price','status','is_deleted','colors','stock_qty']
        fields = ['name','slug','price','colors','stock_qty','brand','category','description','is_deleted']
        
        
class ProductBrandForm(forms.ModelForm):
    class Meta:
        model =Brand
        fields ="__all__"
        
class ProductCategoryForm(forms.ModelForm):
    slug= forms.CharField(widget=forms.TextInput(attrs={**inputfield_style}))
    name= forms.CharField(widget=forms.TextInput(attrs={**inputfield_style}))
    status = forms.ChoiceField(choices=[  (1, 'Active'),
        (0, 'Inactive')],widget=forms.Select(attrs={**inputfield_style}))
    class Meta:
        model =Category
        fields ="__all__"


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model =ProductReview
        fields ="__all__"

    

class ProductImagesForm(forms.Form):
    image1 = forms.ImageField(
     
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        required=False,
        label="Image 1",
        # help_text="Select an image (JPG, JPEG, PNG).",
        widget=forms.FileInput(attrs={**imagefield_style})
    )
    image2 = forms.ImageField(
    
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        required=False,
        label="Image 2",
        
        # help_text="Select an image (JPG, JPEG, PNG).",
        widget=forms.FileInput(attrs={**imagefield_style}),
        
    )
    image3 = forms.ImageField(
    
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        required=False,
        label="Image 3",
        # help_text="Select an image (JPG, JPEG, PNG).",
        widget=forms.FileInput(attrs={**imagefield_style})
    )
    image4 = forms.ImageField(
     
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        required=False,
        label="Image 5",
        # help_text="Select an image (JPG, JPEG, PNG).",
        widget=forms.FileInput(attrs={**imagefield_style})
    )
    

    def clean(self):
        cleaned_data = super().clean()
        images = [cleaned_data.get(f'image{i}') for i in range(1, 5) if cleaned_data.get(f'image{i}')]
        if len(images) > 4:
            raise forms.ValidationError("You can upload a maximum of 4 images.")
        for image in images:
            if image and image.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError(f"{image.name} exceeds the 5MB size limit.")
        cleaned_data['images'] = images
        return cleaned_data
  