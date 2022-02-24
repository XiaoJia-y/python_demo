# from django import views
from django.contrib import admin
from django.urls import path
from trip import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Login),
    path('index', views.index),
    path('login', views.Login),
    path('login_judge', views.Login_judge),
    path('insert_user', views.Ins_user),
    path('insert_judge', views.Ins_judge),
    path('update_user', views.Update_user),
    path('delete_user', views.Delete_user),
    path('user', views.User),
    path('select', views.select_data),
    path('汕头p1', views.Show_data),
    path('广州p1', views.Show_data),
    path('北京p1', views.Show_data),
    path('深圳p1', views.Show_data),
    path('上海p1', views.Show_data),
    path('日本p1', views.Show_data),
    path('其它p1', views.Show_data),
    path('搜索p1', views.Show_wait_date),
    path('test', views.Test)
    # path('搜索', views.async_view),s
]
