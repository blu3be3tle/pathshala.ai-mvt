from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Like
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied


class PostListView(ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        return super().get_queryset().select_related("user").order_by("-created_at")


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related('user')
            .prefetch_related('likes')
            .annotate(like_count=Count('likes'))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = self.object
        user = self.request.user

        context['is_liked'] = (
            user.is_authenticated
            and post.likes.filter(user=user).exists()
        )

        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Post'
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Post'
        return context


class PostDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = Post
    template_name = 'posts/delete_confirm.html'
    success_url = reverse_lazy('post_list')


@login_required
@require_POST
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)

    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        like.delete()

    return redirect('post_detail', pk=pk)
