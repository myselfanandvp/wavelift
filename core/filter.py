import django_filters
from products.models import Product

class IndexProductFilter(django_filters.FilterSet):
    class Meta:
        model=Product
        