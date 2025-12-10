from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth.decorators import login_required

# Create your views here.


def post_list(request):
    posts = Post.objects.select_related("user").all().order_by("-created_at")
    return render(request, "posts/post_list.html", {"posts": posts})


def post_detail(request, pk):
    post = Post.objects.get(id=pk)
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
