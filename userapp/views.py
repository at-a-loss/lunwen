import json
import os
import uuid
import time

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from redis import Redis

from userapp.models import Users, Dept

re = Redis(host='127.0.0.1', port=6379)
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
    name=request.GET.get("name")
    if id or name:
        user1=Users.objects.filter(id=id)
        user2=Users.objects.filter(name=name)
        user=user1 | user2

    else:
        user=Users.objects.all()
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

def get_status(request):
    sel = "<select>"
    sel += "<option value='工作'>工作</option>"
    sel += "<option value='退休'>退休</option>"
    sel += "</select>"
    return HttpResponse(sel)

@csrf_exempt
def opener(request):
    freeze=request.POST.get("freeze")
    oper=request.POST.get("oper")
    id = request.POST.get("id")
    phone = request.POST.get("phone")
    dept_id = request.POST.get("dept_id")
    if oper=="edit":
        u = Users.objects.get(pk=id)
        u.phone=phone
        u.dept_id=Dept.objects.get(name=dept_id)
        if freeze=="工作":
            u.freeze=1
        else:
            u.freeze = 0
        u.save()
    return HttpResponse("1")

def get_data(request):


    try:
        b1 = int(re.get("b1"))
        b2 = int(re.get("b2"))
        b3 = int(re.get("b3"))
        b4 = int(re.get("b4"))
        b5 = int(re.get("b5"))
    except:
        (b1,b2,b3,b4,b5)=get_a()
    # 从数据库中查询对应的日期以及日期对应的用户的数据并转json

    data = {
        "x": ["第一周", "第二周", "第三周", "第四周", "第五周"],
        "y": [b5, b4, b3, b2, b1]
    }

    return JsonResponse(data)

def get_a():
    b1=b2=b3=b4=b5=0
    users=Users.objects.all()
    for user in users:
        t1=time.time()
        time_array=time.strptime(user.create_time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        if int((t1-int(time.mktime(time_array)))/(3600*24)/7)==0:
            b1+=1
        elif int((t1-int(time.mktime(time_array)))/(3600*24)/7)==1:
            b2+=1
        elif int((t1-int(time.mktime(time_array)))/(3600*24)/7)==2:
            b3+=1
        elif int((t1-int(time.mktime(time_array)))/(3600*24)/7)==3:
            b4+=1
        elif int((t1-int(time.mktime(time_array)))/(3600*24)/7)==4:
            b5+=1
    re.setex("b1",3600*24,b1)
    re.setex("b2",3600*24,b2)
    re.setex("b3",3600*24,b3)
    re.setex("b4",3600*24,b4)
    re.setex("b5",3600*24,b5)
    return (b1,b2,b3,b4,b5)

def get_map(request):
    data=re.get("datas")
    if data:
        data=json.loads(data)
    else:
        data = [
            {"name": '北京', "value": 0},
            {"name": '天津', "value": 0},
            {"name": '上海', "value": 0},
            {"name": '重庆', "value": 0},
            {"name": '河北', "value": 0},
            {"name": '河南', "value": 0},
            {"name": '云南', "value": 0},
            {"name": '辽宁', "value": 0},
            {"name": '湖南', "value": 0},
            {"name": '安徽', "value": 0},
            {"name": '山东', "value": 0},
            {"name": '新疆', "value": 0},
            {"name": '江苏', "value": 0},
            {"name": '浙江', "value": 0},
            {"name": '江西', "value": 0},
            {"name": '湖北', "value": 0},
            {"name": '广西', "value": 0},
            {"name": '甘肃', "value": 0},
            {"name": '山西', "value": 0},
            {"name": '陕西', "value": 0},
            {"name": '吉林', "value": 0},
            {"name": '福建', "value": 0},
            {"name": '贵州', "value": 0},
            {"name": '广东', "value": 0},
            {"name": '青海', "value": 0},
            {"name": '西藏', "value": 0},
            {"name": '四川', "value": 0},
            {"name": '宁夏', "value": 0},
            {"name": '海南', "value": 0},
            {"name": '台湾', "value": 0},
            {"name": '香港', "value": 0},
            {"name": '内蒙古', "value": 0},
            {"name": '黑龙江', "value": 0},
        ]
        data=map(data)
    return JsonResponse(data, safe=False)

def map(datas):
    c=0
    for data in datas:
        count=Users.objects.filter(addr1=data["name"]).count()
        print(count)
        datas[c]["value"]=count
        c+=1
    re.setex("datas",24*3600,json.dumps(datas))
    return datas

def getdept(request):
    dept=Dept.objects.values_list("name",flat=True)
    sel="<select>"
    for i in dept:
        sel+=f"<option>{i}</option>"
    sel+="</select>"
    return HttpResponse(sel)

def user_default(u):
    if isinstance(u,Users):
        if u.gender:
            gender="男"
        else:
            gender="女"
        if u.freeze:
            freeze = "工作"
        else:
            freeze = "退休"
        return {"id":u.id,"name":u.name,"gender":gender,"create_time":u.create_time.strftime("%Y-%m-%d %H:%M:%S"),"head":u.head.url,"phone":u.phone,"addr":u.addr2,"freeze":freeze,"dept_id":u.dept_id.name}