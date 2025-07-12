from django.urls import path
from .views import SignupUser
urlpatterns=[
    path('signup/',SignupUser.as_view(),name="signup_url")
]