from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from django.contrib.auth.decorators import login_required
from .forms import PostForm
# Create your views here.


def post_list(request):
    posts = Post.objects.select_related("user").all().order_by("-created_at")
    return render(request, "posts/post_list.html", {"posts": posts})


def post_detail(request, pk):
    post = get_object_or_404(Post.objects.select_related("user"), pk=pk)
    return render(request, "posts/post_detail.html", {"post": post})


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
        return redirect('post_list')

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
        return redirect('post_list')

    if request.method == "POST":
        post.delete()
        return redirect('post_list')

    return render(request, 'posts/delete_confirm.html', {'post': post})
