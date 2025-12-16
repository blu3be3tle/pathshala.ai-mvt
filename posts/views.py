from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Like
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden
from django.views.generic import ListView
# Create your views here.
from django.db.models import Count


class PostListView(ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        return super().get_queryset().select_related("user").order_by("-created_at")


def post_detail(request, pk):
    post = get_object_or_404(
        Post.objects.select_related(
            "user").prefetch_related('likes').annotate(like_count=Count('likes')),
        pk=pk
    )
    is_liked = False
    if request.user.is_authenticated:
        is_liked = post.likes.filter(user=request.user).exists()
    return render(request, "posts/post_detail.html", {
        "post": post,
        "is_liked": is_liked
    })


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("post_list")

    else:
        form = PostForm()

    return render(request, "posts/post_form.html", {'form': form, 'title': 'Create Post'})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.user != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/post_form.html', {
        'form': form,
        'title': 'Edit Post'
    })


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        post.delete()
        return redirect('post_list')

    return render(request, 'posts/delete_confirm.html', {'post': post})


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
