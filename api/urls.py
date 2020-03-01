from django.urls import path
from . import views

urlpatterns = [
    path('create-model', views.create_model),
]
