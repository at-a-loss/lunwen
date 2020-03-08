from django.urls import path
from indexapp import views
app_name="indexapp"
urlpatterns = [
    path("index/",views.index,name="index"),
    path("login/",views.login,name="login"),
    path("get_code/",views.get_code,name="get_code"),
    path("loginlogic/",views.loginlogic,name="loginlogic"),
    path("add_pic/",views.add_pic,name="add_pic"),
    path("data/",views.data,name="data"),
    path("opener/",views.opener,name="opener"),
    path("get_status/",views.get_status,name="get_status"),
]