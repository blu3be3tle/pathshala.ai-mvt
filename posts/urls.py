from django.urls import path
from .views import post_create, post_detail, post_list

urlpatterns = [
    path('', post_list, name="post_list"),
    path('post/<int:pk>', post_detail, name="post_detail"),
    path('create', post_create, name="post_create")
]
