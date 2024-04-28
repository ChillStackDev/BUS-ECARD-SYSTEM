from django.urls import path
from .views import *
urlpatterns = [
    path('',index,name='index'),
    path('home',home,name="home"),
    path('openLogin',openLogin,name="openLogin"),
    path('application',application,name="application"),
    path('login',login_a,name='login'),
    path('logout',logout_a,name="logout"),
    path('reset',reset,name='reset'),
    path('enter_otp',enter_otp,name="enter_otp"),
    path('password_changed',password_changed,name="password_changed")
]
