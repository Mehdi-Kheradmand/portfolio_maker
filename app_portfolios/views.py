import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from portfolio_maker.tools import is_ajax, bad_request_ajax_error, is_it_correct_name, is_image, is_valid_date, \
    is_valid_url, is_it_numeric, get_file_extension
from .models import Portfolio


def show_portfolio_view(req, user):
    return render(request=req, template_name="app_portfolios_templates/dashboard.html")


@login_required
def edit_portfolio_view(req):
    the_user: User = req.user
    cont = {
        'portfolio_link': the_user.useradditional.portfolio_link,
        'post_url': reverse("app_portfolios:UrlsSavePortfolio"),
    }

    return render(request=req, template_name="app_portfolios_templates/dashboard.html", context=cont)


@login_required
def save_portfolio(req):
    if not is_ajax(req):
        return bad_request_ajax_error()
    response = {}

    # read Items from Ajax request
    portfolio_items = {
        'first_name': req.POST.get('first_name').strip(),
        'last_name': req.POST.get('last_name').strip(),
        'profile_image': req.FILES.get('profile_image'),
        'user_skill_title': req.POST.get('user_skill_title').strip(),
        'introduce': req.POST.get('introduce').strip(),
        'about_me_title': req.POST.get('about_me_title').strip(),
        'work_experience': req.POST.get('work_experience').strip(),
        'birthday': req.POST.get('birthday').strip(),
        'website': req.POST.get('website').strip(),
        'freelance': req.POST.get('freelance').strip(),
        'phone': req.POST.get('phone').strip(),
        'linkedin': req.POST.get('linkedin').strip(),
        'instagram': req.POST.get('instagram').strip(),
    }

    if validate_portfolio(portfolio_items):
        # Select or create portfolio
        user_portfolio = Portfolio.objects.filter(owner_id=req.user.id)

        if user_portfolio.count() == 0:
            new_portfolio = Portfolio.objects.create(
                owner_id=req.user.id,
                first_name=portfolio_items['first_name'],
                last_name=portfolio_items['last_name'],
                user_skill_title=portfolio_items['user_skill_title'],
                introduce=portfolio_items['introduce'],
                about_me_title=portfolio_items['about_me_title'],
                work_experience=portfolio_items['work_experience'],
                website=portfolio_items['website'],
                freelance=portfolio_items['freelance'],
                phone=portfolio_items['phone'],
                linkedin=portfolio_items['linkedin'],
                instagram=portfolio_items['instagram'],
            )
            # birthday
            if portfolio_items['birthday']:
                new_portfolio.birthday = portfolio_items['birthday']

            # profile Image
            profile_image = portfolio_items['profile_image']
            if profile_image:
                # Ensure directory structure exists
                directory = 'images/profile_images/' + req.user.useradditional.portfolio_link
                os.makedirs(directory, exist_ok=True)

                with open(directory + get_file_extension(profile_image.name), 'wb') as f:
                    for chunk in profile_image.chunks():
                        f.write(chunk)
                new_portfolio.profile_image = req.user.useradditional.portfolio_link + get_file_extension(profile_image.name)
            new_portfolio.save()
        else:
            user_portfolio = user_portfolio.first()
            user_portfolio.first_name = portfolio_items['first_name']
            user_portfolio.last_name = portfolio_items['last_name']
            user_portfolio.user_skill_title = portfolio_items['user_skill_title']
            user_portfolio.introduce = portfolio_items['introduce']
            user_portfolio.about_me_title = portfolio_items['about_me_title']
            user_portfolio.work_experience = portfolio_items['work_experience']
            user_portfolio.website = portfolio_items['website']
            user_portfolio.freelance = portfolio_items['freelance']
            user_portfolio.phone = portfolio_items['phone']
            user_portfolio.linkedin = portfolio_items['linkedin']
            user_portfolio.instagram = portfolio_items['instagram']

            # birthday
            if portfolio_items['birthday']:
                user_portfolio.birthday = portfolio_items['birthday']

            # save image
            profile_image = portfolio_items['profile_image']
            if profile_image:
                # Ensure directory structure exists
                directory = 'images/profile_images/' + req.user.useradditional.portfolio_link
                os.makedirs(directory, exist_ok=True)

                with open(directory + get_file_extension(profile_image.name), 'wb') as f:
                    for chunk in profile_image.chunks():
                        f.write(chunk)
            user_portfolio.profile_image = req.user.useradditional.portfolio_link + get_file_extension(profile_image.name)

            user_portfolio.save()
    else:
        return bad_request_ajax_error()

    return JsonResponse(response, status=200)


def validate_portfolio(portfolio_items) -> bool:
    if not is_it_correct_name(name=portfolio_items['first_name']) and portfolio_items['first_name'] != '':
        return False
    if not is_it_correct_name(portfolio_items['last_name']) and portfolio_items['last_name'] != '':
        return False

    if portfolio_items['profile_image']:
        if not is_image(portfolio_items['profile_image'].name):
            return False

    if len(portfolio_items['user_skill_title']) > 50:
        return False
    if len(portfolio_items['introduce']) > 60000:
        return False
    if len(portfolio_items['about_me_title']) > 200:
        return False
    if len(portfolio_items['work_experience']) > 60000:
        return False
    if not is_valid_date(portfolio_items['birthday']) and portfolio_items['birthday'] != '':
        return False
    if portfolio_items['website']:
        if not is_valid_url(portfolio_items['website']) or len(portfolio_items['website']) > 150:
            return False
    if len(portfolio_items['freelance']) > 50:
        return False

    if portfolio_items['phone']:
        if not is_it_numeric(portfolio_items['phone']):
            return False

    if portfolio_items['linkedin']:
        if not is_valid_url(portfolio_items['linkedin']) or len(portfolio_items['linkedin']) > 50:
            return False

    if portfolio_items['instagram']:
        if not is_valid_url(portfolio_items['instagram']) or len(portfolio_items['instagram']) > 50:
            return False
    return True
