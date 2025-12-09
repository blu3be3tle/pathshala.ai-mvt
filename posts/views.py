from django.shortcuts import render, redirect

# Create your views here.


def post_list(request):
    post = Post.object.select_related("user").all().order_by("-created_at")
    return render(request, "posts/post_list.html", {"post": post})


def post_detail(request, pk):
    post = Post.object.get(id=pk)
    return render(request, "posts/post_detail.html", {"post": post})


def post_create(request, pk):
    if request.method == "POST":
        content = request.POST.get("content")
        Post.objects.create(user=request.user, content=content)
        return redirect("post_list")

    return render(request, "posts/posts_create.html")
