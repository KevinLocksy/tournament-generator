from django.shortcuts import render, redirect
from django.contrib.auth import login, views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . import logger


def signup(request):
    if request.user.is_authenticated:
        logger.info(
            "Sign up - User is authenticated and logged in. Redirects to home page"
        )
        return redirect("home")
    if request.method == "POST":
        logger.info("Sign up - POST")
        form = UserCreationForm(request.POST)
        if form.is_valid():
            logger.info("Sign up - Form valid")
            user = form.save()
            login(request, user)
            messages.success(request, "Signup successful! You are now logged in.")
            logger.info("Sign up - Successful")
            return redirect("home")
    else:
        logger.info("Sign up - Page")
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})


class CustomLoginView(auth_views.LoginView):
    """Custom class overriding LoginView's dispatch method to avoid accessing login page when user is logged in"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logger.info(
                "Log in - User is authenticated and logged in. Redirects to home page"
            )
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
