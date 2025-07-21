from .views import AdminDashboard,ListUser,UserDetails
from django.urls import path

urlpatterns=[
    path('dashboard/',AdminDashboard.as_view(),name="admin_dashboard_url"),
    path('list/',ListUser.as_view(),name="user_list_url"),
    path('details/<uuid:id>',UserDetails.as_view(),name='user_details_url'),
   
]