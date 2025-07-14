from django.urls import path
from .views import HomePage,Contactus,Aboutus

urlpatterns =[
    path('',HomePage.as_view(),name="index_page"),
    path('contact/',Contactus.as_view(),name="contact_page"),
    path('about/',Aboutus.as_view(),name="about_page"),
]