from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, toggle_like

urlpatterns = [
    path('', PostListView.as_view(), name="post_list"),
    path('create', PostCreateView.as_view(), name="post_create"),
    path('post/<int:pk>', PostDetailView.as_view(), name="post_detail"),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name="post_edit"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="post_delete"),
    path('post/<int:pk>/like/', toggle_like, name="toggle_like")
]
