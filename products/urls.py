from django.urls import path
from .views import CreateProudctView,CreateCategory
urlpatterns=[
    path("create/",CreateProudctView.as_view(),name="create_proudct_url"),
    path("category/",CreateCategory.as_view(),name="create_category_url"),
]