from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from uuid import uuid4
from django.core.exceptions import ValidationError
from django.conf import settings
from colorfield.fields import ColorField

def validate_file_size(value):
    max_size = 5 * 1024 * 1024  # 5MB
    if value.size > max_size:
        raise ValidationError('File size must be less than 5MB.')

class Category(models.Model):
    STATUS_CHOICES = (
        (1, 'Active'),
        (0, 'Inactive'),
    )
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255)  # Renamed from type
    slug = models.CharField(max_length=255, unique=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.name}"

class Brand(models.Model):
    STATUS_CHOICES = (
        (1, 'Active'),
        (0, 'Inactive'),
    )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'brands'
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.name}"
    
    
# class Color(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
#     name = models.CharField(max_length=50, unique=True)
#     hex_code = models.CharField(max_length=7, help_text="Hex code (e.g. #FFFFFF)")

#     class Meta:
#         db_table = 'colors'
#         verbose_name = 'Color'
#         verbose_name_plural = 'Colors'
#         ordering = ['name']

#     def __str__(self):
#         return f"{self.name} ({self.hex_code})"



class ProductColor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    color = ColorField(default='#FFFFFF')
    name = models.CharField(max_length=50,unique=True,blank=False,null=False)

    class Meta:
        db_table = 'product_colors'
        verbose_name = 'Product Color'
        verbose_name_plural = 'Product Colors'
        ordering = ['color']
        
    def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    STATUS_CHOICES = (
        (1, 'Active'),
        (0, 'Inactive'),
    )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    is_deleted = models.BooleanField(default=False)
    colors = models.ManyToManyField(ProductColor, related_name='products', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stock_qty = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
            models.Index(fields=['brand']),
        ]

    def __str__(self):
        return f"{self.name}"

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     if not self.images.filter(is_primary=True).exists() and self.images.exists():
    #         first_image = self.images.first()
    #         first_image.is_primary = True
    #         first_image.save()

class ProductImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to='product_images/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png']), validate_file_size]
    )
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_images'
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
        

    def __str__(self):
        return f"Image for {self.product.name}"

class ProductReview(models.Model):
    STATUS_CHOICES = (
        (1, 'Active'),
        (0, 'Inactive'),
    )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_reviews')    
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    
    review = models.TextField(max_length=5000)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product_reviews'
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"Review for {self.product.name} by {self.user}"
