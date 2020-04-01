import json
import os
import uuid
import time

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from attendanceapp.models import Attendance, Title
from userapp.models import Users, Dept

# def a(request):
#     return render(request, "a.html")
#
# @csrf_exempt
# def b(request):
#     a=request.FILES.get("a")
#     a.name = str(uuid.uuid4()) + os.path.splitext(a.name)[1]
#     for i in range(1,100):
#         Users.objects.create(name="张三"+str(i),password="123",gender=1,phone="13011128324",addr1="北京市",addr2="北京市西城区",head=a,freeze=1)
#     return HttpResponse("1")


def data(request):
    num=request.GET.get("page")
    rownum=request.GET.get("rows")
    id=request.GET.get("id")
    bm=request.GET.get("bm")
    name=request.GET.get("name")
    users=Users.objects.filter(dept_id=Dept.objects.get(id=bm)).filter(freeze=1)
    if id or name:
        user1=users.filter(id=id)
        user2=users.filter(name=name)
        user=user1 | user2
    else:
        user=users
    pagtor=Paginator(user,rownum)
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
    yj = request.POST.get("yj")
    if oper=="edit":
        u = Users.objects.get(pk=id)
        u.performance=yj
        u.save()
    return HttpResponse("1")


def user_default(u):
    if isinstance(u,Users):
        if u.gender:
            gender="男"
        else:
            gender="女"
        mon = time.localtime(time.time()).tm_mon
        year = time.localtime(time.time()).tm_year
        count1,count2,count3,count4=0,0,0,0
        count1+=Attendance.objects.filter(create_time__year=year,create_time__month=int(mon),user_id=u,title_id=Title.objects.get(pk=1)).count()
        count2+=Attendance.objects.filter(create_time__year=year,create_time__month=int(mon),user_id=u,title_id=Title.objects.get(pk=2)).count()
        count3+=Attendance.objects.filter(create_time__year=year,create_time__month=int(mon),user_id=u,title_id=Title.objects.get(pk=3)).count()
        count4+=Attendance.objects.filter(create_time__year=year,create_time__month=int(mon),user_id=u,title_id=Title.objects.get(pk=4)).count()
        salary=int(u.dept_id.salary)-count1*50-count2*50-count3*50-count4*50
        if u.dept_id.id==1:
            salary+=3*u.performance
        elif u.dept_id.id==3:
            salary+=4*u.performance
        if count1 and count2 and count3 and count4:
            pass
        else:
            salary+=200
        return {"id":u.id,"name":u.name,"gender":gender,"head":u.head.url,"dept_id":u.dept_id.name,"bj":count1,"sj":count2,"cd":count3,"zt":count4,"yj":u.performance,"salary":salary}