from django.shortcuts import render
from django.views.generic import View

from django.contrib.auth import login,authenticate
from django.contrib.auth.hashers import make_password
from .forms import RegisterForm
# Create your views here.


def signin(req):
    return render(req, "login/login.html", {})


class SigninView(View):
    def get(self,req):
        return render(req, "login/login.html", {})

    def post(self,req):
        email = req.POST.get("email","")
        pwd = req.POST.get("password","")
        user = authenticate(username=email,password=pwd)
        if user:
            login(req,user)  #cookie,session设置
            return render(req,"login/index.html",)
        else:
            return render(req, "login/login.html", {"msg":"用户名或密码错误"})

class IndexView(View):
    def get(self,req):
        return render(req,"login/index.html",{})





def register(req):
    return render(req, "login/register.html", {})


class RegisterView(View):
    def get(self,req):
        register_form = RegisterForm()
        return render(req,"login/register.html",{"register_form":register_form})

