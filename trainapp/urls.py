from django.urls import path
from userapp import views
app_name="userapp"
urlpatterns = [
    # path("a/",views.a,name="a"),
    # path("b/",views.b,name="b"),
    path("data/",views.data,name="data"),
    path("get_status/",views.get_status,name="get_status"),
    path("opener/",views.opener,name="opener"),
    path("get_data/",views.get_data,name="get_data"),
    path("get_map/",views.get_map,name="get_map"),
    path("getdept/",views.getdept,name="getdept"),
]