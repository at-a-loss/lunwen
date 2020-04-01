import json
import time

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from redis import Redis

from attendanceapp.models import *
from userapp.models import Users, Dept
re = Redis(host='127.0.0.1', port=6379)
def data(request):
    num=request.GET.get("page")
    rownum=request.GET.get("rows")
    id = request.GET.get("id")
    name = request.GET.get("name")
    if not id:
        id=0
    if id or name:
        user1 = Attendance.objects.filter(user_id__id=id)
        user2 = Attendance.objects.filter(user_id__name=name)
        attendance=(user1 | user2).order_by("-create_time")
    else:
        attendance=Attendance.objects.all().order_by("-create_time")
    pagtor=Paginator(attendance,rownum)
    page=pagtor.page(num)
    data={
        "page":num,
        "total":pagtor.num_pages,
        "records":pagtor.count,
        "rows":list(page)
    }
    users=json.dumps(data,default=user_default)
    return HttpResponse(users)

@csrf_exempt
def opener(request):
    oper=request.POST.get("oper")
    id = request.POST.get("id")
    title = request.POST.get("title")
    if oper=="edit":
        u = Attendance.objects.get(pk=id)
        u.title=Title.objects.get(title=title)
        u.save()
    elif oper=="del":
        u = Attendance.objects.get(pk=id)
        u.delete()
    return HttpResponse("1")

def editAttendance(request):
    status = request.GET.get("status")
    id = request.GET.get("id")
    print(id,status)
    try:
        u = Attendance.objects.create(title=Title.objects.get(pk=status),user_id=Users.objects.get(pk=id))
        return HttpResponse("1")
    except:
        return HttpResponse("0")

def get_title(request):
    dept=Title.objects.values_list("title",flat=True)
    sel="<select>"
    for i in dept:
        sel+=f"<option>{i}</option>"
    sel+="</select>"
    return HttpResponse(sel)

def get_data(request):
    mon=time.localtime(time.time()).tm_mon
    a,b,c,d=0,0,0,0
    atts=Attendance.objects.all()
    # 从数据库中查询对应的日期以及日期对应的用户的数据并转json
    for att in atts:
        time_array = time.strptime(att.create_time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        if time_array.tm_mon==mon:
            if att.title.title=="病假":
                a+=1
            elif att.title.title=="事假":
                b += 1
            elif att.title.title=="迟到":
                c += 1
            elif att.title.title=="早退":
                d += 1
    data = {
        "x": ["病假", "事假", "迟到","早退"],
        "y": [a, b, c,d]
    }
    return JsonResponse(data)

def user_default(u):
    if isinstance(u,Attendance):
        return {"id":u.id,"uid":u.user_id.id,"name":u.user_id.name,"create_time":u.create_time.strftime("%Y-%m-%d %H:%M:%S"),"head":u.user_id.head.url,"phone":u.user_id.phone,"title":u.title.title,"dept_id":u.user_id.dept_id.name}