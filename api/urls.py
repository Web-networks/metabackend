from django.urls import path
from . import views

urlpatterns = [
    path('create-model', views.create_model),
    path('start-train-task', views.start_train_task),
]
