from django.urls import path
from app_users.views import login_view, register_view, logout_view

urlpatterns = [
    path('login', login_view, name="UrlsLogin"),
    path('register', register_view, name="UrlsRegister"),
    path('logout', logout_view, name="UrlsLogout"),

]

app_name = "app_users"
