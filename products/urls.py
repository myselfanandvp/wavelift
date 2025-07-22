from django.urls import path
from .views import CreateProudctView,CreateCategory,ListProductView
urlpatterns=[
    path("create/",CreateProudctView.as_view(),name="create_proudct_url"),
    path("category/",CreateCategory.as_view(),name="create_category_url"),
    path("products/",ListProductView.as_view(),name="list_products_url"),
]