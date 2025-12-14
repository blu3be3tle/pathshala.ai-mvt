from django.urls import path
from .views import post_create, post_detail, post_list, post_delete, post_edit, toggle_like

urlpatterns = [
    path('', post_list, name="post_list"),
    path('create', post_create, name="post_create"),
    path('post/<int:pk>', post_detail, name="post_detail"),
    path('post/<int:pk>/edit/', post_edit, name="post_edit"),
    path('post/<int:pk>/delete/', post_delete, name="post_delete"),
    path('post/<int:pk>/like/', toggle_like, name="toggle_like")
]
