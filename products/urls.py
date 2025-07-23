from django.urls import path
from .views import CreateProudctView,CreateCategory,ListProductView,EditProductView,ListCategory,DeleteCategory,EditCategory
urlpatterns=[
    path("create/",CreateProudctView.as_view(),name="create_proudct_url"),
    path("category/",CreateCategory.as_view(),name="create_category_url"),
    path("list/",ListProductView.as_view(),name="list_products_url"),
    path("edit/<uuid:product_id>",EditProductView.as_view(),name="edit_products_url"),
    path("category/list/",ListCategory.as_view(),name="list_category_url"),
    path("category/delete/<uuid:id>",DeleteCategory.as_view(),name="delete_category_url"),
    path("category/edit/<uuid:id>",EditCategory.as_view(),name="edit_category_url"),
    
]