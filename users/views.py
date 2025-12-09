from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import login

# Create your views here.


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        login(request, user)
        return redirect("post_list")

    return render(request, "users/signup.html")

