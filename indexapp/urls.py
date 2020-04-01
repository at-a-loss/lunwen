from django.urls import path
from indexapp import views
app_name="indexapp"
urlpatterns = [
    path("index/",views.index,name="index"),
    path("login/", views.login, name="login"),
    path("captcha/", views.captcha, name="captcha"),
    path("captchaAjax/", views.captchaAjax, name="captchaAjax"),
    path("loginlogic/", views.loginlogic, name="loginlogic"),
    path("loginAjax/", views.loginAjax, name="loginAjax"),
]