from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import RegisterForm

def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created.")
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "registrar/register.html", {"form": form})
