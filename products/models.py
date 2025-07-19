from django.db import models
from uuid import uuid4
# Create your models here.


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stock_qty = models.IntegerField()

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"{self.name}"

class Product_images(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid4,editable=False)
    product = models.ForeignKey(Product,on_delete=models.CASCADE ,related_name='images')
    image = models.ImageField(upload_to='product_images/')
    alt_text= models.CharField(max_length=255,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table= 'product_images'
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
    def __str__(self):
        return f"Image for {self.product.name}"