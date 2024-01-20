from django.shortcuts import render


def show_portfolio_view(req, p_username):
    return render(request=req, template_name="app_portfolios_templates/dashboard.html")


def edit_portfolio_view(req):
    print(123)
