import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(
           label='Status',
        choices=[
            ('', 'All'),
            (1, 'Active'),
            (0, 'Not Active')
        ], empty_label=None 
    )
    name = django_filters.ChoiceFilter(
        label='Product Name'
    )
    class Meta:
        model =Product
        fields=['name','status','category','brand']
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        product_names = Product.objects.values_list('name', 'name').distinct()
        self.filters['name'].extra['choices'] = product_names