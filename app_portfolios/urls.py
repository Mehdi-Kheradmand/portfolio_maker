from django.urls import path
from .views import edit_portfolio_view, save_portfolio

urlpatterns = [
    path('EditPortfolio', edit_portfolio_view, name="UrlsEditPortfolio"),
    path('SavePortfolio', save_portfolio, name="UrlsSavePortfolio"),
    # path('<p_username>', show_portfolio_view, name="UrlsShowPortfolio"),
]

app_name = "app_portfolios"
