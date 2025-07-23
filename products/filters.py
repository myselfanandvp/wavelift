import django_filters
from .models import Product, Color, Category
from django import forms


class ProductFilter(django_filters.FilterSet):
    is_deleted = django_filters.ChoiceFilter(
        label='Status',
        choices=[
            ('', 'All'),
            (0, 'Active'),
            (1, 'Not Active')
        ], empty_label=None
    )
    name = django_filters.ChoiceFilter(
        label='Product Name',
         
    )
    colors = django_filters.ModelMultipleChoiceFilter(
        queryset=Color.objects.all(),

    )
    
    

    class Meta:
        model = Product
        fields = ['name', 'category', 'brand', 'colors', 'is_deleted']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        product_names = Product.objects.values_list('name', 'name').distinct()
        self.filters['name'].extra['choices'] = product_names


class CategoryFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(
        label='Status',
        choices=[
            ("", "All"),
            (1, "Active"),
            (0, "Inactive"),
        ],
        empty_label=None,
        widget=forms.Select(
            attrs={
                'class': 'fg-gray-50 border border-gray-500 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'
            }
        )
    )
    name = django_filters.CharFilter(lookup_expr='icontains', label="Name", widget=forms.TextInput(
        attrs={
            'class': 'fg-gray-50 border border-gray-500 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'
        }
    ))
    slug = django_filters.CharFilter(lookup_expr="icontains", label='Slug', widget=forms.TextInput(
        attrs={
            'class': 'fg-gray-50 border border-gray-500 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'

        }
    ))

    id = django_filters.CharFilter(lookup_expr="icontains", label='ID', widget=forms.TextInput(
        attrs={
            'class': 'fg-gray-50 border border-gray-500 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'

        }
    ))

    class Meta:
        model = Category
        fields = ['id', 'slug', 'status', 'name']
