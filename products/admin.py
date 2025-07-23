from django.contrib import admin
from .models import Product,ProductImage,ProductReview,Brand,Category,Color
# Register your models here.

admin.site.register([Product,ProductImage,ProductReview,Brand,Category,Color])
