from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login ,logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .models import UploadedFile
from .forms import UploadBookForm


@login_required(login_url='login')
def home(request):
    return render(request,'home.html')


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get("password1")
        pass2 = request.POST.get("password2")
        public_visibility = request.POST.get('publicv') == "on"
        CustomUser.objects.all().delete()
        if pass1 != pass2:
            return HttpResponse("Your password does not match")
        else:
            my_user = CustomUser.objects.create_user(
                username=username, email=email, password=pass1, public_visibility=public_visibility)
            return redirect("login")
    return render(request, 'register.html')



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


def authors(request):
    author = CustomUser.objects.filter(public_visibility=True)
    return render(request, 'author.html', {'author': author})


def sellers(request):
    Sellers = CustomUser.objects.filter(public_visibility=True)
    return render(request, 'sellers.html', {'Sellers': Sellers })

def upload_book(request):
    if request.method=="POST":
        form = UploadBookForm(request.POST,request.FILES)
        if form.is_valid():
            UploadedFile = form.save(commit=False)
            if request.user.is_authenticated:
                UploadedFile.user_id = request.user_id
            UploadedFile.save()
            return redirect('upload_book')
        else:
            form = UploadBookForm()
        return render(request, 'upload_book.html', {'form': form})
    return render(request, 'upload_book.html')


    # if request.method=="POST":
    #     form = UploadFileForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         user_id = form.cleaned_data['user_id']
    #         title = form.cleaned_data['title']
    #         visibility = form.cleaned_data['visibility']
    #         description = form.cleaned_data['description']
    #         cost = form.cleaned_data['cost']
    #         year_of_published = form.cleaned_data['year_of_published']
    #         file = form.cleaned_data['file']
    #         uploaded_file = UploadedFile.objects.create(
    #             user_id=user_id,title=title,visibility=visibility,description=description,cost=cost,year_of_published=year_of_published
    #             ,file=file
    #         )
    #         return redirect('home')
    #     else:
    #         form = UploadFileForm()
    #     return render(request,'upload_book.html',{'form':form})
