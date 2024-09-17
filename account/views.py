from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django_email_verification import send_email
from .forms import LoginForm, UserCreateForm, UserUpdateForm

User = get_user_model()


def register_user(request: HttpRequest):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = form.save(commit=False)
            user_email = form.cleaned_data.get("email")
            user_username = form.cleaned_data.get("username")
            user_password = form.cleaned_data.get("password1")
            if not user_email or not user_username or not user_password:
                raise Exception("Invalid form submission")
            user = User.objects.create_user(
                username=user_username, email=user_email, password=user_password
            )
            user.is_active = False
            send_email(user)
            return redirect("/account/email-verification-sent/")
    else:
        form = UserCreateForm()
    return render(request, "account/registration/register.html", {"form": form})


def login_user(request: HttpRequest):
    form = LoginForm()
    if request.user.is_authenticated:
        return redirect("shop:products")
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("account:dashboard")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("account:login")

    return render(request, "account/login/login.html", {"form": form})


def logout_user(request: HttpRequest):
    logout(request)
    return redirect("shop:products")


@login_required(login_url="account:login")
def dashboard_user(request: HttpRequest):
    return render(request, "account/dashboard/dashboard.html")


@login_required(login_url="account:login")
def profile_user(request: HttpRequest):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("account:dashboard")
    else:
        form = UserUpdateForm(instance=request.user)
    return render(
        request, "account/dashboard/profile-management.html", {"form": form}
    )


@login_required(login_url="account:login")
def delete_user(request: HttpRequest):
    # user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        request.user.delete()
        return redirect("shop:products")
    return render(request, "account/dashboard/account-delete.html")
