from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from userPanel.models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django_email_verification import sendConfirm
from django.core.mail import send_mail
from GreenDivision.env import Forget_subject, Forget_body, ignore_message


def user_login(request):
    if request.method == "GET":
        return render(request, "userPanel/login.html")
    else:
        email = request.POST.get("email")
        password = request.POST.get("password")
        profile = Profile.objects.get(email=email)
        user = authenticate(username=profile.user.username, password=password)

        if user:
            login(request, user)
            return redirect("user:index")
        else:
            msg = "Error"
            return render(request, "userPanel/login.html", {"msg": msg})


def sign_up(request):
    if request.method == "GET":
        return render(request, "userPanel/register.html")
    else:
        name = request.POST.get("name")
        email = request.POST.get("email")
        varsity_id = request.POST.get("id")
        username = request.POST.get("username")
        url = request.POST.get("url")
        password = request.POST.get("password")

        user = User.objects.create(
            username=username, password=password, email=email, is_active=False
        )
        user.set_password(password)
        user.save()
        Profile.objects.create(
            user=user, name=name, email=email, varsity_id=varsity_id, uri_link=url
        )
        sendConfirm(user)

        return redirect("login")


@login_required
def user_logout(request):
    logout(request)
    return redirect("user:index")