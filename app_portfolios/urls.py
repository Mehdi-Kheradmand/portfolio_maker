from django.urls import path
from .views import edit_portfolio_view, show_portfolio_view

urlpatterns = [
    path('<p_username>', show_portfolio_view, name="UrlsShowPortfolio"),
    path('dashboard', edit_portfolio_view, name="UrlsEditPortfolio"),
]

app_name = "app_portfolios"
