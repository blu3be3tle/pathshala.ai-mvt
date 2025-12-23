from django.contrib.auth import get_user_model
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import login, authenticate, logout
from .forms import ProfileUpdateForm
User = get_user_model()


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


def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("post_list")

    return render(request, "users/login.html")


def logout(request):
    logout(request)
    return redirect("login")


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/profile.html"

    def get_object(self):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileUpdateForm
    template_name = "users/profile_edit.html"
    success_url = "/profile/"

    def get_object(self):
        return self.request.user
