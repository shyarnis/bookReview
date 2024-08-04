from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.db import IntegrityError

from accounts.forms import UserCreateForm


# Create your views here.
def signup_account(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreateForm()})

    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"]
                )
                user.save()
                login(request, user)
                return redirect("home_page")

            except IntegrityError:  # username already exists.
                return render(
                    request,
                    "signup.html",
                    {
                        "form": UserCreateForm,
                        "error": "Username already taken. Choose new username.",
                    },
                )

        else:  # passwords don't match.
            return render(
                request,
                "signup.html",
                {"form": UserCreateForm, "error": "Passwords do not match"},
            )


def login_account(request):
    if request.method == "GET":
        return render(request, "login.html", {"form": AuthenticationForm()})

    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )

        if user is None:  # username and password do not match.
            return render(
                request,
                "login.html",
                {
                    "form": AuthenticationForm(),
                    "error": "username and password do not match",
                },
            )
        else:
            login(request, user)
            return redirect("home_page")


def logout_account(request):
    logout(request)
    return redirect("home_page")
