from django.urls import path
from . import views

urlpatterns = [
    path('create-model', views.create_model),
    path('start-train-task', views.start_train_task),
    path('start-eval-task', views.start_eval_task),
    path('upload-user-input', views.upload_user_input),
]
