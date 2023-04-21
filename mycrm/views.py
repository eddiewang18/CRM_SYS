from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

@login_required
def home(request):

    return render(request,"home.html")


def login_view(request):
    context = {
        
    }
    if request.method=="GET":
        form = AuthenticationForm(request)
    else:
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect("/")
        else:
            context['wrong']='帳號或密碼錯誤'
    context['form']=form
    return render(request,'login.html',context)

def logout_view(request):
    logout(request)
    return redirect('/')
