from django.urls import path
from .views import AdminDashboard,ListProducts

urlpatterns=[
    path('dashboard/',AdminDashboard.as_view(),name="admin_dashboard_url"),
    path('listproducts/',ListProducts.as_view(),name="list_products_url")
]