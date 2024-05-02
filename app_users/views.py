from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .models import UserAdditional
from portfolio_maker.tools import email_to_url
import re


def login_view(req):
    cont = {"input_error": False}

    if req.user.is_authenticated:
        return redirect("UrlsHomePage")

    if req.method == "POST":
        received_email = req.POST.get("email")
        received_password = req.POST.get("password")
        # check inputs
        if not (check_email(received_email) and check_password(received_password)):
            cont["input_error"] = True
        else:
            found_user = User.objects.filter(username__exact=received_email)
            if found_user.count() == 1:
                if found_user.first().check_password(raw_password=received_password):
                    login(request=req, user=found_user.first())
                    return redirect("UrlsHomePage")
            cont["input_error"] = True

    # showing loginPage
    return render(req, "app_users_templates/login.html", cont)


def register_view(req):
    if req.user.is_authenticated:
        return redirect("UrlsHomePage")

    cont = {"pass_match_error": False, "already_exist_error": False, "invalid_input_error": False}
    if req.method == "POST":
        received_email = req.POST.get("email")
        received_password = req.POST.get("password")
        received_re_password = req.POST.get("re-password")

        # check matching passwords
        if received_password != received_re_password:
            cont["pass_match_error"] = True
            return render(req, "app_users_templates/register.html", cont)

        # check values (username and password)
        if not (check_email(received_email) and check_password(received_password)):
            cont["invalid_input_error"] = True
            return render(req, "app_users_templates/register.html", cont)

        # check for being unique
        q = User.objects.filter(username__exact=received_email)

        if q.count() != 0:  # username already exist
            cont["already_exist_error"] = True
            return render(req, "app_users_templates/register.html", cont)

        # values are OK then create and login new user
        new_user_creator: User = User.objects.create_user(
            username=received_email,
            password=received_password,
            email=received_email,
        )
        new_user_creator.save()

        # find unique portfolio link
        portfolio_link = email_to_url(received_email, add_random_num=True)
        q = UserAdditional.objects.filter(portfolio_link=portfolio_link)
        while q.count() != 0:
            q = UserAdditional.objects.filter(portfolio_link=portfolio_link)

        # create user additional
        additional_creator = UserAdditional.objects.create(
            owner_id=new_user_creator.id,
            portfolio_link=portfolio_link,
        )
        additional_creator.save()

        login(request=req, user=new_user_creator)
        return redirect("UrlsHomePage")
    else:
        return render(req, "app_users_templates/register.html", cont)


def logout_view(req):
    logout(req)
    return redirect("/")


def check_email(email):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(email_regex, email):
        return True
    else:
        return False


def check_password(password):
    if password:
        if len(password) < 8 or len(password) > 50:
            return False
        return True
    return False
