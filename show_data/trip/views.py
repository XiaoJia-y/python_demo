from django.shortcuts import render, redirect
from django.http import HttpResponse
import MySQLdb
from trip.models import Data, Login_table, User_table
from django.contrib.auth import login
from functools import wraps
import urllib
import sys
import time
sys.path.append("../")
from get_data.Get_data import Get_data
from get_data import Conect_sql
import json
# import asyncio
# import nest_asyncio
# nest_asyncio.apply()

place = ""
num = 0

def init(request):
    return render(request, 'index.html')

def Login(request):
    return render(request, 'login.html')

def check_login(f):
    @wraps(f)
    def inner(request,*arg,**kwargs):
        if request.session.get('is_login')=='1':
            return f(request,*arg,**kwargs)
        else:
            return redirect('/login/')
    return inner
 
def Login_judge(request):
 # 如果是POST请求，则说明是点击登录按扭 FORM表单跳转到此的，那么就要验证密码，并进行保存session
    if request.method=="POST":
        user_name=request.POST.get('user_name')
        pass_word=request.POST.get('pass_word')
        user=Login_table.objects.filter(user_name=user_name,pass_word=pass_word)
    if user:
    #登录成功
    # 1，生成特殊字符串
    # 2，这个字符串当成key，此key在数据库的session表（在数据库存中一个表名是session的表）中对应一个value
    # 3，在响应中,用cookies保存这个key ,(即向浏览器写一个cookie,此cookies的值即是这个key特殊字符）
        request.session['is_login']='1' # 这个session是用于后面访问每个页面（即调用每个视图函数时要用到，即判断是否已经登录，用此判断）
        # request.session['username']=username # 这个要存储的session是用于后面，每个页面上要显示出来，登录状态的用户名用。
        # 说明：如果需要在页面上显示出来的用户信息太多（有时还有积分，姓名，年龄等信息），所以我们可以只用session保存user_id
        request.session['user_name']=user[0].user_name
        return redirect('/index')
 # 如果是GET请求，就说明是用户刚开始登录，使用URL直接进入登录页面的
    flag = 0
    return render(request,'login.html', context={'flag' : flag})
 
@check_login
def index(request):
 # students=Students.objects.all() ## 说明，objects.all()返回的是二维表，即一个列表，里面包含多个元组
 # return render(request,'index.html',{"students_list":students})
 # username1=request.session.get('username')
    user_name=request.session.get('user_name')
    # 使用user_id去数据库中找到对应的user信息
    if user_name == 'admin':
        return render(request, 'manage.html', {"flag": 1})
    else:
        return render(request, 'manage.html', {'flag': 0})
    # user_name = request.POST['user_name']
    # pass_word = request.POST['pass_word']
    # data = Data.objects.all()
    # if user_name and pass_word:
    #     num = Login_table.objects.filter(user_name = user_name, pass_word = pass_word).count()
    #     if num == 1:
    #         if user_name == 'admin':
    #             flag = 1
    #             return render(request, 'manage.html' , context = {'user_name' : user_name, 'pass_word' : pass_word, 'flag' : flag})
    #         else:
    #             flag = 0
    #             return render(request, 'manage.html' , context = {'user_name' : user_name, 'pass_word' : pass_word, 'flag' : flag})
    #     else:
    #         flag = 0
    #         return render(request, 'login.html' , context = {'user_name' : user_name, 'pass_word' : pass_word, 'flag' : flag})
    # else:
    #     flag = 0
    #     return render(request, 'login.html' , context = {'user_name' : user_name, 'pass_word' : pass_word, 'flag' : flag})

def Ins_user(request):
    # user_name = request.POST['user_name']
    # pass_word = request.POST['pass_word']
    return render(request, 'insert_user.html')

def Ins_judge(request):
    user_name = request.POST['username']
    pass_word = request.POST['password']
    name = request.POST['name']
    num = Login_table.objects.filter(user_name = user_name).count()
    if user_name and pass_word and num == 0:
        num1 = Login_table(user_name = user_name, pass_word = pass_word)
        num2 = User_table(name = name, user_name = user_name, pass_word = pass_word)
        num1.save()
        num2.save()
        data = User_table.objects.all()
        return render(request, 'user.html', context={'data' : data})
    else:
        flag = 0
        return render(request, 'insert_user.html', context={'flag' : flag})

def User(request):
    # user_name = request.POST['user_name']
    # pass_word = request.POST['pass_word']
    # if user_name == 'admin':
    data = User_table.objects.all()
    # return render(request, 'user.html', context = {'user_name' : user_name, 'data' : data, 'pass_word' : pass_word})
    return render(request, 'user.html', context = {'data' : data})
    # else:
    #     return HttpResponse("你没有权限访问")

def Update_user(request):
    update_name = request.POST['name']
    update_user_name = request.POST['username']
    update_pass_word = request.POST['password']
    id = request.POST['id']
    Login_table.objects.filter(id = id).update(user_name = update_user_name, pass_word = update_pass_word)
    User_table.objects.filter(id = id).update(name = update_name, user_name = update_user_name, pass_word = update_pass_word)
    data = User_table.objects.all()
    return render(request, 'user.html', context = {'data' : data})

def Delete_user(request):
    delete = request.POST['id']
    User_table.objects.filter(id = delete).delete()
    Login_table.objects.filter(id = delete).delete()
    data = User_table.objects.all()
    return render(request, 'user.html', context = {'data' : data})

def Show_data(request):
    user_name=request.session.get('user_name')
    if user_name == 'admin':
        flag = 1
    else:
        flag = 0
    global place, num
    url = request.get_full_path()
    name = urllib.parse.unquote(url)
    href = name[1:-2]
    href1 = name[1:-2]
    if href == "其它":
        num = int(num)
        G = Get_data()
        data = G.main(place, num)
        conn = MySQLdb.Connect(host = "42.193.255.161", port = 3306, user = 'root', passwd = '123456', db = 'trip', charset="utf8")
        s = Conect_sql.Save_data()
        s.insert_data(conn, data)
        href1 = place
    data = Data.objects.values().filter(name__contains = href1)
    data = list(data)
    return render(request, '{href}.html'.format(href = href), context = {'data' : data, 'flag' : flag, name : href})

def select_data(request):
    user_name=request.session.get('user_name')
    if user_name == 'admin':
        flag = 1
    else:
        flag = 0
    return render(request, "select.html", context = {'flag' : flag})

# async def Show_select_data(request, place, num, i):
#     await asyncio.sleep(1)
#     user_name=request.session.get('user_name')
#     if user_name == 'admin':
#         flag = 1
#     else:
#         flag = 0
#     num = int(num)
#     # Show_wait_date(request, num)
#     num += 2
#     url = request.get_full_path()
#     name = urllib.parse.unquote(url)
#     href = name[1::]
#     href1 = name[1::]
#     if i == 2:
#         G = Get_data()
#         data = G.main(place, num)
#         conn = MySQLdb.Connect(host = "42.193.255.161", port = 3306, user = 'root', passwd = '123456', db = 'trip', charset="utf8")
#         s = Conect_sql.Save_data()
#         s.insert_data(conn, data)
#         data = Data.objects.filter(name__contains = place)
#         return render(request, '{href}.html'.format(href = href1), context = {'data' : data, 'flag' : flag, name : href})
#     elif i == 1:
#         time = num * 6 + 1
#         print(time)
#         return render(request, 'wait.html', context = {'flag' : flag, 'time' : time, 'name' : place})
    # return redirect('/汕头')
    # return render(request, '{href}.html'.format(href = href1), context = {'data' : data, 'flag' : flag, name : href})
def Show_wait_date(request):
    global place
    user_name=request.session.get('user_name')
    if user_name == 'admin':
        flag = 1
    else:
        flag = 0
    place = request.POST["data"]
    num = request.POST["num"]
    num = int(num)
    time = num * 6 + 1
    return render(request, 'wait.html', context = {'flag' : flag, 'time' : time, 'name' : place})
    
# def Show_wait_date(request):
#     user_name=request.session.get('user_name')
#     if user_name == 'admin':
#         flag = 1
#     else:
#         flag = 0
#     place = request.POST["data"]
#     num = request.POST["num"]
#     num = int(num)
#     # Show_wait_date(request, num)
#     url = request.get_full_path()
#     name = urllib.parse.unquote(url)
#     # href = name[1::]
#     # href1 = name[1::]
#     num += 2
#     G = Get_data()
#     data = G.main(place, num)
#     conn = MySQLdb.Connect(host = "42.193.255.161", port = 3306, user = 'root', passwd = '123456', db = 'trip', charset="utf8")
#     s = Conect_sql.Save_data()
#     s.insert_data(conn, data)
#     # data = Data.objects.filter(name__contains = place)
#     time = num * 6 + 1
#     return render(request, 'wait.html', context = {'flag' : flag, 'time' : time, 'name' : place})

# async def async_view(request):
#     place = request.POST["data"]
#     num = request.POST["num"]
#     num = int(num)
#     user_name=request.session.get('user_name')
#     if user_name == 'admin':
#         flag = 1
#     else:
#         flag = 0
#     time1 = num * 6 + 1
#     # loop.create_task(Show_wait_date(request, num))
#     loop = asyncio.get_event_loop()
#     tasks = []
#     for i in range(1,3):
#         task = loop.create_task(Show_wait_date(request, place, num))
#         tasks.append(task)
#     wait_coro = asyncio.wait(tasks)
#     loop.run_until_complete(wait_coro)
    # loop.close()   
    # loop.create_task(Show_wait_date(request, num))
    # return render(request, 'wait.html', context = {'flag' : flag, 'time' : time1, 'name' : place})
    
def Test(request):
    return render(request, 'test.html')
