from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login ,logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser,UploadedFile
from .models import UploadedFile
from .forms import UploadBookForm
from django.contrib import messages
from MyApp.models import UploadedFile
from django.shortcuts import render
from sqlalchemy import text
from sqlalchemy import create_engine
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import LoginSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
import datetime
import jwt
from .serializers import UserSerializer
from .serializers import BookSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .utils import send_otp, login_d


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
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            if send_otp(request, user.email):
                request.session['username'] = username
                # request.session['user'] = user
                auth_login(request, user)
                token = genrate_jwt_token(user)
                return redirect("verify_otp")
            
        else:
            return HttpResponse("Username or Password is incorrect!!!")
    return render(request, "login.html")

def verify_otp(request):
    if request.method=="POST":
        user_entered_otp = request.POST.get('otp')
        user_entered_otp = int(user_entered_otp)

        session_otp = request.session.get('otp')
        session_otp = int(session_otp)

        email1 = "venkateshpensalwar2507@gmail.com"

        if session_otp == user_entered_otp:
            login_d(request,email1)
            return redirect('home')
        else:
            messages.success(request,"Wrong Otp")
    return render(request, "verify_otp.html")


def logout_page(request):
    logout(request)
    return redirect("login")

#this is token generate code
def genrate_jwt_token(user):
    payload = {
        "id":user.id,
        "exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
        "iat":datetime.datetime.utcnow(),
    }
    return jwt.encode(payload, 'secret', algorithm="HS256")


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
                UploadedFile.user_id = request.user.id
            UploadedFile.save()
            messages.success(request,'Your book has been uploaded successfully!')
            return redirect('upload_book')
    form = UploadBookForm()
    return render(request, 'upload_book.html', {'form': form})


@login_required(login_url='login')
def view_book(request):
    view_books = UploadedFile.objects.all()
    return render(request, "view_book.html", {'view_books': view_books})


@csrf_exempt
@login_required(login_url='login')
def view_user_books(request):
    view_books = UploadedFile.objects.filter(
        visibility=True, user_id=request.user.id)
    return render(request, "view_users_books.html", {'view_books': view_books})


def fetch_data(request):
    # DATABASE_URL = 'postgresql://postgres:root123@localhost/socail_book'
    NAME = 'socail_book'
    USER = 'postgres'
    PASSWORD = 'root123'
    HOST = 'localhost'
    PORT = '5432'

    engine = create_engine(f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}')

    with engine.connect() as connection:
        sql_query = text(
            """SELECT * FROM public."MyApp_uploadedfile" ORDER BY id ASC;""")
        result = connection.execute(sql_query)
        # result = pd.read_sql_query(sql_query,engine)
        print(result)
        view_books = result.fetchall()
    return render(request, 'enginedata.html', {'view_books': view_books})


def logout_view(request):
    logout(request)
    return redirect('index')

def send_email_to_client(request):
    subject = "ThiS Email is from Django Server"
    message = "Hello! This email is from Django server!"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ["venkateshpensalwar2000@gmail.com"]
    send_mail(subject, message, from_email, recipient_list)
    return HttpResponseRedirect(reverse('home'))

def send_email(subject,message,recipient_list):
    send_email(
        subject,
        message,
        settings.EMAIL_HOST_USER
        ,recipient_list
    )

def send_email():
    send_email_to_client()
    return redirect('/')

#All View Functions are Created Here
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        # user = CustomUser.objects.filter(username=username).first()
        user = authenticate(request,username=username,password=password)
        if user is None:
            raise AuthenticationFailed('User does not exist')
        token = genrate_jwt_token(user)
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password')
        # payload = {
        #     'id': user.id,
        #     'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        #     'iat': datetime.datetime.utcnow(),
        # }
        # token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response({'token':token,'message':"Login Successfull"})
        response.set_cookie('jwt', token)
        return response
        # response.set_cookie(key='jwt', value=token, httponly=True)
        # response.data = {'jwt': token} 
        
       

class UserView(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        token = request.COOKIES.get("jwt")
        if not token:
            raise AuthenticationFailed('Unauthenticated...')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        except jwt.DecodeError:
            raise AuthenticationFailed('Invalid token!')
        
        user = CustomUser.objects.filter(id=payload["id"]).first()
        if not user:
            raise AuthenticationFailed('User Not found')
        serializer = UserSerializer(user)
        return Response(serializer.data)


class BookUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request,*args, **kwargs):
        token = request.COOKIES.get("jwt")
        if not token:
            raise AuthenticationFailed(
                'Authentication credentials were not provided.')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Invalid authentication credentials!')
        except jwt.DecodeError:
            raise AuthenticationFailed('Invalid authentication credentials!')
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)