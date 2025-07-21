from django.urls import path
from .views import CreateProudctView
urlpatterns=[
    path("create/",CreateProudctView.as_view(),name="create_proudct_url"),
]