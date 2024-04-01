from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login

def home(request):
    return render(request,'home.html')

def register(request):
    if request.metod == "POST":
        username = request.POST.get("username")
        email = request.POST.get('email')
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        user = User.objects.create_user(username=username, password1=password1,password2=password2, email=email)  
        
    return render(request,'register.html')

def login(request):
    # if request.method == "POST":
    #     username = request.POST.get("username")
    #     password = request.POST.get("password")
    #     user =  authenticate(request,username=username, password=password)
    #     if user is not None:
    #         auth_login(request,user)
    #         return render(request,"login_success.html")
    #     else:
    #         error_message = "Invalid username or password"
    #         return render(request,"login.html",{'error':error_message})
    return render(request,"login.html")

