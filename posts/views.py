from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from django.contrib.auth.decorators import login_required

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
        content = request.POST.get("content")
        Post.objects.create(user=request.user,
                            content=content,
                            title="Untitled Post")
        return redirect("post_list")

    return render(request, "posts/post_create.html")
