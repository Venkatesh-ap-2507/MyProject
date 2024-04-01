from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login ,logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def home(request):
    return render(request,'home.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get('email')
        pass1 = request.POST.get("password1")
        pass2 = request.POST.get("password2")

        if pass1!=pass2:
            return HttpResponse("Your password does not match")
        else:
            my_user = User.objects.create_user(username, email, pass1)
            my_user.save()
            return redirect("login")
    return render(request,'register.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        pass1 = request.POST.get("pass")
        user =  authenticate(request,username=username, password=pass1)
        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            return HttpResponse("Username or Password is incorrect!!!")
    return render(request,"login.html")

def logout_page(request):
    logout(request)
    return redirect("login")